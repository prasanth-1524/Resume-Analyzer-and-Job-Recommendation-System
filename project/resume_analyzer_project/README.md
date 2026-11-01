# Resume Analyzer and Job Recommendation System
# python app.py
A final-year BCA web application that extracts text from PDF/DOCX resumes, detects skills, compares a resume with sample job descriptions, recommends relevant jobs, highlights missing skills, and lets signed-in users save jobs and review analysis history.

## Features
- Registration and login with hashed passwords
- PDF and DOCX resume upload (5 MB maximum)
- Resume text extraction
- Rule-based skill detection using a starter vocabulary
- Resume-to-job matching with skill coverage and TF-IDF cosine similarity
- Job search, recommendations, saved jobs, and analysis history
- SQLite database initialized automatically
- Sample job listings seeded on first run
- Unit tests for core analyzer logic

## Requirements
- Python 3.11+
- pip
- VS Code or another editor
- Internet is not required after Python packages are installed

## Run locally (Windows PowerShell)
```powershell
cd resume_analyzer_project
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:SECRET_KEY = "replace-this-with-a-long-random-secret"
python app.py
```
Open http://127.0.0.1:5000 in your browser.

### Run locally (macOS/Linux)
```bash
cd resume_analyzer_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export SECRET_KEY="replace-this-with-a-long-random-secret"
python app.py
```

The database file `resume_analyzer.db` is created automatically. Five sample jobs are inserted if they do not already exist.

## Demo flow
1. Register an account with a password of at least 8 characters.
2. Log in and open Dashboard.
3. Upload a text-based PDF or DOCX resume.
4. Review detected skills and ranked sample jobs.
5. Open a job to view matched and missing skills.
6. Save the analysis to history and save a job to the dashboard.

## Important implementation notes
- The job listings are sample data for academic demonstration. They are not live vacancies.
- The matching score is a heuristic similarity score, not a hiring probability or guarantee.
- Scanned/image-only PDFs need OCR; this starter version expects selectable text in the PDF.
- The vocabulary is deliberately small and should be expanded for a stronger final submission.
- This starter project does not include a full admin UI. Add job management as an extension if required.
- For production use, add CSRF protection, rate limiting, stronger secret management, virus scanning, privacy/retention controls, secure deployment settings, and access-controlled file downloads.
- Uploaded files are stored locally and extracted resume text is stored in SQLite. Do not upload sensitive real resumes to a public demo.

## Project structure
```text
resume_analyzer_project/
├── app.py
├── analyzer.py
├── database.py
├── requirements.txt
├── README.md
├── docs/
│   ├── project_report.md
│   ├── database_design.md
│   ├── testing.md
│   ├── viva_questions.md
│   └── diagrams.md
├── templates/
├── static/css/style.css
├── tests/test_analyzer.py
└── uploads/
```

## Tests
```bash
pytest -q
```

## Database tables
`users`, `resumes`, `skills`, `resume_skills`, `jobs`, `job_skills`, `analysis_results`, `saved_jobs`.

## Troubleshooting
- **`ModuleNotFoundError`:** Activate the virtual environment and run `pip install -r requirements.txt`.
- **PDF text is empty:** The PDF may be scanned. Use a text-based PDF or add OCR support.
- **Port 5000 is busy:** Change `app.run(debug=True, port=5001)` at the bottom of `app.py`.
- **Reset sample database:** Stop the server, delete `resume_analyzer.db`, then restart the app. This deletes local accounts and uploaded resume metadata.
