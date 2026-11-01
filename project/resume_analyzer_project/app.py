import os
import re
import sqlite3
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from analyzer import extract_resume_text, analyze_resume_against_job, extract_skills
from database import get_db, init_db, seed_jobs, close_db

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-development-secret")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
UPLOAD_DIR.mkdir(exist_ok=True)

app.teardown_appcontext(close_db)

with app.app_context():
    init_db()
    seed_jobs()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(413)
def too_large(_error):
    flash("File is too large. Maximum allowed size is 5 MB.", "danger")
    return redirect(url_for("upload_resume"))


@app.route("/")
def index():
    db = get_db()
    jobs = db.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT 3").fetchall()
    return render_template("index.html", jobs=jobs)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Enter your name, a valid email, and a password of at least 8 characters.", "danger")
            return render_template("register.html")
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (name, email, generate_password_hash(password), datetime.utcnow().isoformat())
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("An account with that email already exists.", "danger")
            return render_template("register.html")
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))
        flash("Incorrect email or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    resumes = db.execute(
        "SELECT * FROM resumes WHERE user_id = ? ORDER BY uploaded_at DESC",
        (session["user_id"],)
    ).fetchall()
    analyses = db.execute("""
        SELECT a.*, j.title AS job_title, j.company, r.original_filename
        FROM analysis_results a
        JOIN jobs j ON j.job_id = a.job_id
        JOIN resumes r ON r.resume_id = a.resume_id
        WHERE a.user_id = ? ORDER BY a.created_at DESC LIMIT 10
    """, (session["user_id"],)).fetchall()
    saved = db.execute("""
        SELECT j.* FROM saved_jobs s JOIN jobs j ON j.job_id = s.job_id
        WHERE s.user_id = ? ORDER BY s.saved_at DESC
    """, (session["user_id"],)).fetchall()
    return render_template("dashboard.html", resumes=resumes, analyses=analyses, saved=saved)


@app.route("/resume/upload", methods=["GET", "POST"])
@login_required
def upload_resume():
    if request.method == "POST":
        file = request.files.get("resume")
        if not file or not file.filename:
            flash("Choose a PDF or DOCX resume.", "danger")
            return redirect(url_for("upload_resume"))
        if not allowed_file(file.filename):
            flash("Unsupported file type. Upload a PDF or DOCX file.", "danger")
            return redirect(url_for("upload_resume"))
        original = secure_filename(file.filename)
        unique_name = f"user{session['user_id']}_{int(datetime.utcnow().timestamp())}_{original}"
        path = UPLOAD_DIR / unique_name
        file.save(path)
        try:
            text = extract_resume_text(path)
            if not text.strip():
                raise ValueError("No readable text found in the file.")
        except Exception as exc:
            path.unlink(missing_ok=True)
            flash(f"Could not read this resume: {exc}", "danger")
            return redirect(url_for("upload_resume"))

        skills = extract_skills(text)
        db = get_db()
        cursor = db.execute("""
            INSERT INTO resumes (user_id, original_filename, stored_filename, extracted_text, uploaded_at)
            VALUES (?, ?, ?, ?, ?)
        """, (session["user_id"], original, unique_name, text, datetime.utcnow().isoformat()))
        resume_id = cursor.lastrowid
        for skill in skills:
            db.execute("INSERT OR IGNORE INTO skills (skill_name) VALUES (?)", (skill,))
            skill_id = db.execute("SELECT skill_id FROM skills WHERE skill_name = ?", (skill,)).fetchone()["skill_id"]
            db.execute("INSERT OR IGNORE INTO resume_skills (resume_id, skill_id) VALUES (?, ?)", (resume_id, skill_id))
        db.commit()
        flash(f"Resume uploaded. Detected {len(skills)} skills.", "success")
        return redirect(url_for("resume_detail", resume_id=resume_id))
    return render_template("upload.html")


@app.route("/resume/<int:resume_id>")
@login_required
def resume_detail(resume_id):
    db = get_db()
    resume = db.execute(
        "SELECT * FROM resumes WHERE resume_id = ? AND user_id = ?",
        (resume_id, session["user_id"])
    ).fetchone()
    if not resume:
        abort(404)
    skills = db.execute("""
        SELECT s.skill_name FROM skills s
        JOIN resume_skills rs ON rs.skill_id = s.skill_id
        WHERE rs.resume_id = ? ORDER BY s.skill_name
    """, (resume_id,)).fetchall()
    jobs = db.execute("SELECT * FROM jobs ORDER BY title").fetchall()
    results = []
    for job in jobs:
        report = analyze_resume_against_job(resume["extracted_text"], job["description"])
        results.append({
            "job": job,
            "score": report["match_score"],
            "matched": report["matched_skills"],
            "missing": report["missing_skills"]
        })
    results.sort(key=lambda item: item["score"], reverse=True)
    return render_template("resume_detail.html", resume=resume, skills=skills, results=results[:10])


@app.route("/jobs")
def jobs():
    q = request.args.get("q", "").strip()
    db = get_db()
    if q:
        pattern = f"%{q}%"
        rows = db.execute("""
            SELECT * FROM jobs WHERE title LIKE ? OR company LIKE ? OR description LIKE ?
            ORDER BY title
        """, (pattern, pattern, pattern)).fetchall()
    else:
        rows = db.execute("SELECT * FROM jobs ORDER BY title").fetchall()
    return render_template("jobs.html", jobs=rows, q=q)


@app.route("/jobs/<int:job_id>")
def job_detail(job_id):
    job = get_db().execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if not job:
        abort(404)
    report = None
    resume = None
    if session.get("user_id"):
        resume = get_db().execute("""
            SELECT * FROM resumes WHERE user_id = ? ORDER BY uploaded_at DESC LIMIT 1
        """, (session["user_id"],)).fetchone()
        if resume:
            report = analyze_resume_against_job(resume["extracted_text"], job["description"])
    saved = False
    if session.get("user_id"):
        saved = get_db().execute(
            "SELECT 1 FROM saved_jobs WHERE user_id = ? AND job_id = ?",
            (session["user_id"], job_id)
        ).fetchone() is not None
    return render_template("job_detail.html", job=job, report=report, resume=resume, saved=saved)


@app.route("/jobs/<int:job_id>/save", methods=["POST"])
@login_required
def save_job(job_id):
    db = get_db()
    if not db.execute("SELECT 1 FROM jobs WHERE job_id = ?", (job_id,)).fetchone():
        abort(404)
    db.execute(
        "INSERT OR IGNORE INTO saved_jobs (user_id, job_id, saved_at) VALUES (?, ?, ?)",
        (session["user_id"], job_id, datetime.utcnow().isoformat())
    )
    db.commit()
    flash("Job saved to your dashboard.", "success")
    return redirect(url_for("job_detail", job_id=job_id))


@app.route("/jobs/<int:job_id>/unsave", methods=["POST"])
@login_required
def unsave_job(job_id):
    db = get_db()
    db.execute("DELETE FROM saved_jobs WHERE user_id = ? AND job_id = ?", (session["user_id"], job_id))
    db.commit()
    flash("Job removed from saved jobs.", "info")
    return redirect(url_for("dashboard"))


@app.route("/analyze/<int:resume_id>/<int:job_id>", methods=["POST"])
@login_required
def save_analysis(resume_id, job_id):
    db = get_db()
    resume = db.execute("SELECT * FROM resumes WHERE resume_id = ? AND user_id = ?",
                        (resume_id, session["user_id"])).fetchone()
    job = db.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if not resume or not job:
        abort(404)
    report = analyze_resume_against_job(resume["extracted_text"], job["description"])
    db.execute("""
        INSERT INTO analysis_results
        (user_id, resume_id, job_id, match_score, matched_skills, missing_skills, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session["user_id"], resume_id, job_id, report["match_score"],
          ", ".join(report["matched_skills"]), ", ".join(report["missing_skills"]),
          datetime.utcnow().isoformat()))
    db.commit()
    flash("Analysis saved to your history.", "success")
    return redirect(url_for("resume_detail", resume_id=resume_id))


if __name__ == "__main__":
    app.run(debug=True)
