# Viva Voce Questions and Answers

### 1. What is the objective of this project?
To compare resume content with sample job descriptions, detect skills, recommend relevant roles, and show possible skill gaps.

### 2. Why did you use Flask?
Flask is a lightweight Python web framework with routing, templates, request handling, and session support, making it suitable for a medium-sized academic project.

### 3. What is NLP?
Natural Language Processing is a field of computing that works with human language. This project uses basic text normalization, vocabulary-based extraction, TF-IDF, and cosine similarity.

### 4. How do you extract text from PDF?
PyMuPDF reads pages and returns selectable text. Image-only/scanned PDFs need OCR, which is not included in this version.

### 5. How do you read DOCX?
The python-docx library reads paragraph and table text from Word documents.

### 6. What is TF-IDF?
Term Frequency–Inverse Document Frequency weights terms by their frequency in a document and how informative they are across the compared documents.

### 7. What is cosine similarity?
It measures the cosine of the angle between two vector representations. A higher value generally indicates more similar term usage.

### 8. How is the matching score calculated?
The current score is 75% detected-skill coverage and 25% TF-IDF cosine similarity. This is a heuristic selected for the demo, not a validated hiring model.

### 9. What is a skill gap?
A skill gap is a known skill detected in the job description but not detected in the resume.

### 10. Why use SQLite?
SQLite is lightweight, serverless, and easy to set up for a local student project. The schema can be adapted for MySQL.

### 11. How are passwords stored?
Werkzeug's password-hashing utilities create a salted hash. The plain-text password is not stored.

### 12. What are primary and foreign keys?
A primary key uniquely identifies a record. A foreign key links a record to another table and helps preserve referential integrity.

### 13. What is the many-to-many relationship in this database?
Resumes and skills are many-to-many through `resume_skills`; jobs and skills are many-to-many through `job_skills`.

### 14. What are the limitations?
The skill vocabulary is limited, scanned PDFs are unsupported, sample jobs are not live, and the score does not predict hiring outcomes.

### 15. How could the project be improved?
Add an admin interface, OCR, synonyms, semantic embeddings, more job data, downloadable reports, and stronger security protections.

### 16. What security features are included?
Password hashing, parameterized SQL, upload extension/size checks, safe filenames, and user ownership checks for resume detail routes. More controls are needed before public deployment.

### 17. Why is the match score not a probability?
The score is based on a hand-designed similarity formula and has not been calibrated against real hiring outcomes.

### 18. What is the purpose of `resume_skills`?
It links resume records and canonical skill records without duplicating each skill string for every resume.

### 19. How do you test the system?
Use pytest for analyzer logic and manual tests for registration, authentication, uploads, job search, saving, and dashboard history.

### 20. What did you learn?
The project integrates Python, web routing, SQL schema design, file extraction, text processing, user sessions, testing, and documentation.
