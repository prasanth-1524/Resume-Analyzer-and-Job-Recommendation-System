import sqlite3
from pathlib import Path
from flask import g, current_app

DB_PATH = Path(__file__).resolve().parent / "resume_analyzer.db"

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS resumes (
    resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL,
    extracted_text TEXT NOT NULL,
    uploaded_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS resume_skills (
    resume_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (resume_id, skill_id),
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (job_id, skill_id),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS analysis_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resume_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    match_score INTEGER NOT NULL,
    matched_skills TEXT NOT NULL,
    missing_skills TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS saved_jobs (
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    saved_at TEXT NOT NULL,
    PRIMARY KEY (user_id, job_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)
    db.commit()
    db.close()


def seed_jobs():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    examples = [
        ("Python Developer Intern", "DemoTech Solutions", "Remote / India",
         "Build Python applications using Python, Flask, REST API, SQL, Git, debugging, testing and problem solving."),
        ("Junior Data Analyst", "InsightWorks", "Hyderabad, India",
         "Analyze datasets using Python, SQL, Excel, statistics, pandas, data visualization, Power BI and communication."),
        ("Frontend Developer Intern", "PixelCraft Studio", "Remote / India",
         "Create responsive interfaces using HTML, CSS, JavaScript, Bootstrap, React, Git, accessibility and testing."),
        ("Machine Learning Intern", "ModelSpring Labs", "Bengaluru, India",
         "Prepare data and train models with Python, pandas, NumPy, scikit-learn, machine learning, statistics and SQL."),
        ("Backend Developer Trainee", "CloudBridge Systems", "Chennai, India",
         "Develop backend services using Python, Flask, REST API, SQL, SQLite, authentication, Git, testing and security.")
    ]
    for title, company, location, description in examples:
        exists = db.execute("SELECT 1 FROM jobs WHERE title = ? AND company = ?", (title, company)).fetchone()
        if not exists:
            db.execute("INSERT INTO jobs (title, company, location, description, created_at) VALUES (?, ?, ?, ?, ?)",
                       (title, company, location, description, "2026-01-01T00:00:00"))
    db.commit()
    db.close()
