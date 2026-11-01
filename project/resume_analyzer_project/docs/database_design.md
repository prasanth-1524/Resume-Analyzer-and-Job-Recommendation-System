# Database Design

## Entity relationship overview
- One user can upload many resumes.
- One resume can contain many skills; one skill can belong to many resumes.
- One job can require many skills; one skill can be associated with many jobs.
- One user can save many jobs; a job can be saved by many users.
- Each analysis result belongs to one user, one resume, and one job.

## Tables

### users
| Column | Type | Constraints | Purpose |
|---|---|---|---|
| user_id | INTEGER | PK, auto increment | User identifier |
| name | TEXT | NOT NULL | Display name |
| email | TEXT | UNIQUE, NOT NULL | Login email |
| password_hash | TEXT | NOT NULL | Hashed password |
| created_at | TEXT | NOT NULL | Registration timestamp |

### resumes
| Column | Type | Constraints | Purpose |
|---|---|---|---|
| resume_id | INTEGER | PK | Resume identifier |
| user_id | INTEGER | FK → users | Owner |
| original_filename | TEXT | NOT NULL | Original safe filename |
| stored_filename | TEXT | NOT NULL | Server-side stored filename |
| extracted_text | TEXT | NOT NULL | Extracted resume text |
| uploaded_at | TEXT | NOT NULL | Upload timestamp |

### skills
| Column | Type | Constraints | Purpose |
|---|---|---|---|
| skill_id | INTEGER | PK | Skill identifier |
| skill_name | TEXT | UNIQUE, NOT NULL | Canonical skill label |

### resume_skills
| Column | Type | Constraints | Purpose |
|---|---|---|---|
| resume_id | INTEGER | PK part, FK → resumes | Resume reference |
| skill_id | INTEGER | PK part, FK → skills | Skill reference |

### jobs
| Column | Type | Constraints | Purpose |
|---|---|---|---|
| job_id | INTEGER | PK | Job identifier |
| title | TEXT | NOT NULL | Role title |
| company | TEXT | NOT NULL | Sample company |
| location | TEXT | NOT NULL | Role location |
| description | TEXT | NOT NULL | Role description |
| created_at | TEXT | NOT NULL | Created timestamp |

### job_skills
| Column | Type | Constraints | Purpose |
|---|---|---|---|
| job_id | INTEGER | PK part, FK → jobs | Job reference |
| skill_id | INTEGER | PK part, FK → skills | Skill reference |

### analysis_results
| Column | Type | Constraints | Purpose |
|---|---|---|---|
| result_id | INTEGER | PK | Analysis identifier |
| user_id | INTEGER | FK → users | Owner |
| resume_id | INTEGER | FK → resumes | Resume analyzed |
| job_id | INTEGER | FK → jobs | Job analyzed |
| match_score | INTEGER | NOT NULL | Heuristic score 0–100 |
| matched_skills | TEXT | NOT NULL | Comma-separated skill list |
| missing_skills | TEXT | NOT NULL | Comma-separated skill list |
| created_at | TEXT | NOT NULL | Analysis timestamp |

### saved_jobs
| Column | Type | Constraints | Purpose |
|---|---|---|---|
| user_id | INTEGER | PK part, FK → users | User reference |
| job_id | INTEGER | PK part, FK → jobs | Job reference |
| saved_at | TEXT | NOT NULL | Saved timestamp |

## SQL notes
The executable schema is defined in `database.py`. Foreign-key checks are enabled on database connections. SQLite uses `INSERT OR IGNORE` to avoid duplicate skills and saved jobs.

## Example queries
```sql
-- List a user's resumes
SELECT resume_id, original_filename, uploaded_at
FROM resumes
WHERE user_id = 1
ORDER BY uploaded_at DESC;

-- Saved jobs for a user
SELECT j.title, j.company, s.saved_at
FROM saved_jobs s
JOIN jobs j ON j.job_id = s.job_id
WHERE s.user_id = 1;

-- Recent analyses
SELECT j.title, a.match_score, a.matched_skills, a.missing_skills
FROM analysis_results a
JOIN jobs j ON j.job_id = a.job_id
WHERE a.user_id = 1
ORDER BY a.created_at DESC;
```
