import os
import sqlite3
import hashlib
import secrets
from pathlib import Path
from datetime import datetime, timedelta, timezone
from io import BytesIO
from uuid import uuid4

from flask import Flask, request, session, redirect, url_for, render_template, flash, abort, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parent
DB_PATH = os.getenv("DATABASE_PATH", str(ROOT / "instance" / "vault.sqlite3"))
STORE = Path(os.getenv("STORAGE_PATH", str(ROOT / "storage" / "encrypted")))
FERNET_KEY = os.getenv("FERNET_KEY", "")
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "development-only-change-this")
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_MB", "25")) * 1024 * 1024
STORE.mkdir(parents=True, exist_ok=True)
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username TEXT UNIQUE NOT NULL,
 password_hash TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS files (
 id TEXT PRIMARY KEY,
 owner_id INTEGER NOT NULL,
 original_name TEXT NOT NULL,
 stored_name TEXT UNIQUE NOT NULL,
 size_bytes INTEGER NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS shares (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 file_id TEXT NOT NULL,
 token_hash TEXT UNIQUE NOT NULL,
 expires_at TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
);
"""

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

with connect() as con:
    con.executescript(SCHEMA)

def encrypt_bytes(data):
    if not FERNET_KEY or FERNET_KEY == "PASTE_GENERATED_FERNET_KEY_HERE":
        raise RuntimeError("FERNET_KEY is not configured in .env")
    return Fernet(FERNET_KEY.encode("utf-8")).encrypt(data)

def decrypt_bytes(data):
    if not FERNET_KEY or FERNET_KEY == "PASTE_GENERATED_FERNET_KEY_HERE":
        raise RuntimeError("FERNET_KEY is not configured in .env")
    try:
        return Fernet(FERNET_KEY.encode("utf-8")).decrypt(data)
    except InvalidToken as exc:
        raise ValueError("Wrong encryption key or encrypted data was modified.") from exc

def digest_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    with connect() as con:
        return con.execute("SELECT id, username FROM users WHERE id=?", (uid,)).fetchone()

def owned_file(file_id, owner_id):
    with connect() as con:
        return con.execute(
            "SELECT * FROM files WHERE id=? AND owner_id=?", (file_id, owner_id)
        ).fetchone()

@app.context_processor
def add_user_to_templates():
    return {"logged_user": current_user()}

@app.get("/")
def index():
    return redirect(url_for("vault")) if current_user() else render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not 3 <= len(username) <= 40 or len(password) < 10:
            flash("Username must be 3–40 characters; password must be at least 10 characters.", "error")
            return render_template("register.html")
        try:
            with connect() as con:
                con.execute(
                    "INSERT INTO users(username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password, method="scrypt"))
                )
        except sqlite3.IntegrityError:
            flash("That username already exists.", "error")
            return render_template("register.html")
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        with connect() as con:
            row = con.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if not row or not check_password_hash(row["password_hash"], password):
            flash("Invalid username or password.", "error")
            return render_template("login.html")
        session.clear()
        session["user_id"] = row["id"]
        return redirect(url_for("vault"))
    return render_template("login.html")

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.get("/vault")
def vault():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    with connect() as con:
        rows = con.execute(
            "SELECT * FROM files WHERE owner_id=? ORDER BY created_at DESC", (user["id"],)
        ).fetchall()
    return render_template("vault.html", files=rows)

@app.post("/upload")
def upload():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename:
        flash("Choose a file first.", "error")
        return redirect(url_for("vault"))
    filename = secure_filename(uploaded.filename)
    data = uploaded.read()
    if not filename or not data:
        flash("Filename must be valid and file must not be empty.", "error")
        return redirect(url_for("vault"))
    file_id = uuid4().hex
    stored_name = file_id + ".enc"
    try:
        ciphertext = encrypt_bytes(data)
    except RuntimeError as exc:
        abort(500, str(exc))
    (STORE / stored_name).write_bytes(ciphertext)
    with connect() as con:
        con.execute(
            "INSERT INTO files(id, owner_id, original_name, stored_name, size_bytes) VALUES (?, ?, ?, ?, ?)",
            (file_id, user["id"], filename, stored_name, len(data))
        )
    flash("File encrypted and uploaded.", "success")
    return redirect(url_for("vault"))

@app.get("/download/<file_id>")
def download(file_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    row = owned_file(file_id, user["id"])
    if not row:
        abort(404)
    path = STORE / row["stored_name"]
    if not path.is_file():
        abort(404)
    try:
        clear_data = decrypt_bytes(path.read_bytes())
    except (ValueError, RuntimeError):
        abort(500, "Could not decrypt file. Check the configured encryption key.")
    return send_file(BytesIO(clear_data), as_attachment=True, download_name=row["original_name"])

@app.post("/share/<file_id>")
def create_share(file_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    row = owned_file(file_id, user["id"])
    if not row:
        abort(404)
    try:
        hours = int(request.form.get("hours", "24"))
    except ValueError:
        hours = 24
    if hours not in (1, 6, 24, 72, 168):
        hours = 24
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=hours)
    with connect() as con:
        con.execute(
            "INSERT INTO shares(file_id, token_hash, expires_at) VALUES (?, ?, ?)",
            (file_id, digest_token(token), expires.isoformat())
        )
    share_url = url_for("shared_download", token=token, _external=True)
    return render_template("share_created.html", share_url=share_url, expires=expires.isoformat())

@app.get("/s/<token>")
def shared_download(token):
    with connect() as con:
        row = con.execute(
            """SELECT f.*, s.expires_at FROM shares s
               JOIN files f ON f.id=s.file_id WHERE s.token_hash=?""",
            (digest_token(token),)
        ).fetchone()
    if not row:
        abort(404)
    try:
        expires = datetime.fromisoformat(row["expires_at"])
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
    except ValueError:
        abort(404)
    if datetime.now(timezone.utc) >= expires:
        abort(410, "This share link has expired.")
    path = STORE / row["stored_name"]
    if not path.is_file():
        abort(404)
    try:
        clear_data = decrypt_bytes(path.read_bytes())
    except (ValueError, RuntimeError):
        abort(500, "Could not decrypt shared file.")
    return send_file(BytesIO(clear_data), as_attachment=True, download_name=row["original_name"])

@app.post("/delete/<file_id>")
def delete_file(file_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    row = owned_file(file_id, user["id"])
    if not row:
        abort(404)
    path = STORE / row["stored_name"]
    if path.exists():
        path.unlink()
    with connect() as con:
        con.execute("DELETE FROM shares WHERE file_id=?", (file_id,))
        con.execute("DELETE FROM files WHERE id=? AND owner_id=?", (file_id, user["id"]))
    flash("File and its share links were deleted.", "success")
    return redirect(url_for("vault"))

@app.errorhandler(413)
def too_large(_error):
    return "Upload too large. Reduce the file size or increase MAX_UPLOAD_MB.", 413

if __name__ == "__main__":
    app.run(debug=True)
