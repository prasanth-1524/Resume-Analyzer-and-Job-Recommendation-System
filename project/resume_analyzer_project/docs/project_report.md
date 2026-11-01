# PROJECT REPORT
## Resume Analyzer and Job Recommendation System

**Degree:** Bachelor of Computer Applications (BCA)  
**Project type:** Web application with basic Natural Language Processing  
**Suggested duration:** 5–7 weeks  
**Student name:** [Enter your name]  
**Register number:** [Enter register number]  
**College:** [Enter college name]  
**Guide:** [Enter guide name]  
**Academic year:** [Enter academic year]

## Certificate
This is to certify that the project titled **“Resume Analyzer and Job Recommendation System”** is a bonafide work carried out by [Student Name] under the guidance of [Guide Name] in partial fulfilment of the requirements for the Bachelor of Computer Applications degree. Replace this sample wording with your institution's required certificate format.

## Declaration
I declare that this project report represents work completed by me for academic purposes. Any third-party libraries, references, and resources used have been acknowledged. [Adapt this declaration to your institution's policy.]

## Acknowledgement
I would like to thank my project guide, department faculty, and institution for their support and feedback during the development of this project.

## Abstract
Students and entry-level candidates may find it difficult to compare their resumes with job requirements and identify missing skills. The Resume Analyzer and Job Recommendation System is a web application designed to make this comparison easier. Users create an account, upload a PDF or DOCX resume, and the system extracts text and detects skills from a predefined vocabulary. It compares resume content with sample job descriptions using skill overlap and TF-IDF cosine similarity. A dashboard displays ranked sample roles, matched skills, missing skills, saved jobs, and analysis history. The application is implemented with Python and Flask, uses SQLite for data storage, and uses PyMuPDF and python-docx for document extraction. The result is an explainable educational prototype; its score is a similarity estimate and not a prediction of employment success.

## 1. Introduction
Recruitment descriptions frequently contain skills, tools, and responsibilities that candidates need to compare against their experience. Manual comparison can be time-consuming, especially for students preparing several applications. This project provides a small decision-support tool that extracts resume text, detects known skills, and ranks a set of sample job descriptions.

### 1.1 Problem statement
Students may not know which of their skills are relevant to a particular role or which skills are absent from their resume. The system provides an automated first-pass comparison and a simple skill-gap report.

### 1.2 Objectives
- Build a web interface for user registration and login.
- Accept PDF and DOCX resumes.
- Extract text and identify skills using a configurable vocabulary.
- Compare resumes against job descriptions.
- Calculate an explainable matching score.
- Display missing skills and recommendations.
- Store saved jobs and analysis history.
- Provide a maintainable database schema and automated tests.

### 1.3 Scope
The project supports text-based PDF and DOCX files and a seeded collection of sample jobs. It is intended for academic demonstration. It does not fetch live jobs, guarantee job suitability, parse every resume format, or replace a human recruiter.

## 2. Existing and Proposed System
### Existing system
Candidates often read job descriptions manually, compare skills themselves, and track opportunities using separate notes or spreadsheets. This can be repetitive and inconsistent.

### Proposed system
The proposed application stores resumes and job records, extracts known skills, computes similarity scores, and provides matched/missing skill lists through a browser-based dashboard.

### Advantages
- Faster first-pass comparison.
- Explicit missing-skill lists.
- Central place for saved jobs and prior analyses.
- Low-cost local deployment.
- Explainable rules suitable for a student project.

## 3. Feasibility Study
### Technical feasibility
Python, Flask, SQLite, and document-processing libraries are widely available and suitable for a small web application.

### Economic feasibility
The project can be developed using open-source software on an existing computer.

### Operational feasibility
The user interface uses standard web forms and does not require advanced technical knowledge.

### Schedule feasibility
A 5–7 week schedule is reasonable for an individual student who already knows basic Python and HTML.

## 4. Requirements
### Hardware
- Computer with a modern dual-core processor or better.
- 4 GB RAM minimum; 8 GB recommended.
- Approximately 1 GB free disk space for development packages and test files.

### Software
- Python 3.11 or newer.
- pip and virtual environment support.
- VS Code or equivalent editor.
- Modern browser.
- Required packages listed in `requirements.txt`.

### Functional requirements
1. The system shall allow a user to register and log in.
2. The system shall validate uploaded file extensions and size.
3. The system shall extract text from PDF and DOCX files.
4. The system shall detect skills from the configured vocabulary.
5. The system shall display sample jobs and allow keyword search.
6. The system shall calculate match scores and identify skill gaps.
7. The system shall let users save jobs and analysis results.
8. The dashboard shall display resumes, saved jobs, and analysis history.

### Non-functional requirements
- Usable in a modern desktop or mobile browser.
- Passwords stored as hashes, not plain text.
- Parameterized SQL queries.
- Clear validation and error messages.
- Reasonable response time for small demo files.
- Local data should be treated as private and deleted when no longer needed.

## 5. System Design
### Architecture
Browser UI → Flask routes/controllers → analysis service and document extractors → SQLite database and local uploads folder.

### Modules
- Authentication: registration, login, logout.
- Resume management: upload, extract, store, list.
- Skill extraction: match terms against the vocabulary.
- Job management: browse and search sample jobs.
- Matching engine: skill coverage and text similarity.
- Recommendations: sort roles by score.
- Dashboard: saved jobs and analysis history.

## 6. Algorithm
1. Read the uploaded document.
2. Extract text from PDF or DOCX.
3. Normalize text to lowercase and collapse whitespace.
4. Detect skills by matching each vocabulary item.
5. Extract known skills from the job description.
6. Compute skill coverage = matched job skills / detected job skills.
7. Compute TF-IDF vectors for the resume and job description.
8. Calculate cosine similarity between the vectors.
9. Calculate final score = 75% skill coverage + 25% text similarity.
10. Display score, matched skills, and missing skills.

If the job description contains no known skills, skill coverage is zero. The current formula is a teaching heuristic and should be validated before any real-world use.

## 7. Database Design
The database contains `users`, `resumes`, `skills`, `resume_skills`, `jobs`, `job_skills`, `analysis_results`, and `saved_jobs`. See `database_design.md` for keys and relationships.

## 8. Implementation
The backend is written in Python using Flask routes. SQLite is initialized automatically. The first launch inserts sample job descriptions. The analyzer uses PyMuPDF for PDF text, python-docx for Word documents, and scikit-learn for TF-IDF similarity. The frontend uses Jinja templates, Bootstrap, and a custom stylesheet.

## 9. Testing
Core analyzer tests are included in `tests/test_analyzer.py`. Manual tests should cover registration, login, file upload, invalid file type, job search, matching, saved jobs, and analysis history. See `testing.md` for a test plan and expected results.

## 10. Limitations
- Skill detection depends on a fixed vocabulary and can miss synonyms or context.
- Scanned PDFs require OCR, which is not included.
- Sample jobs are not live listings.
- TF-IDF similarity does not understand meaning as well as modern semantic models.
- Scores are not hiring probabilities and may be affected by resume formatting and keyword choice.
- The prototype requires additional security and privacy controls before public deployment.

## 11. Future Enhancements
- Admin panel for adding and editing jobs.
- OCR for scanned resumes.
- Skill synonyms and occupation-specific taxonomies.
- Semantic embeddings and multilingual resume support.
- Downloadable PDF analysis report.
- Learning-resource links for missing skills.
- MySQL deployment and cloud hosting.
- CSRF protection, rate limiting, audit logging, file scanning, and configurable data retention.

## 12. Conclusion
The Resume Analyzer and Job Recommendation System demonstrates how a web application can combine file processing, database design, text analysis, and a recommendation workflow. It provides an explainable comparison between a resume and sample job descriptions and identifies skills worth reviewing. The prototype meets its educational goals while leaving clear paths for stronger NLP, security, and production readiness.

## References
- Flask documentation: https://flask.palletsprojects.com/
- Python documentation: https://docs.python.org/3/
- scikit-learn documentation: https://scikit-learn.org/stable/
- PyMuPDF documentation: https://pymupdf.readthedocs.io/
- python-docx documentation: https://python-docx.readthedocs.io/
- SQLite documentation: https://www.sqlite.org/docs.html
