import re
from pathlib import Path

# Starter vocabulary: extend this list for the job domain and your college demo.
SKILL_VOCABULARY = {
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "html", "css",
    "bootstrap", "react", "node.js", "flask", "django", "fastapi", "sql", "mysql",
    "sqlite", "postgresql", "mongodb", "git", "github", "rest api", "api",
    "data analysis", "data visualization", "machine learning", "deep learning",
    "scikit-learn", "pandas", "numpy", "excel", "power bi", "tableau", "statistics",
    "communication", "problem solving", "testing", "debugging", "authentication",
    "cybersecurity", "linux", "docker", "aws", "azure", "oop", "data structures",
    "algorithms", "computer networks", "operating systems"
}


def extract_resume_text(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        import fitz
        doc = fitz.open(path)
        return "\n".join(page.get_text("text") for page in doc)
    if suffix == ".docx":
        from docx import Document
        doc = Document(path)
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" ".join(cell.text for cell in row.cells))
        return "\n".join(parts)
    raise ValueError("Only PDF and DOCX files are supported.")


def extract_skills(text):
    normalized = re.sub(r"\s+", " ", text.lower())
    found = []
    for skill in sorted(SKILL_VOCABULARY, key=len, reverse=True):
        # Word boundaries help prevent matching "java" inside "javascript".
        pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"
        if re.search(pattern, normalized):
            found.append(skill)
    return sorted(set(found))


def analyze_resume_against_job(resume_text, job_description):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    # Skill coverage score is explainable: matching required skills / detected job skills.
    # TF-IDF provides a secondary textual similarity score; final score weights both.
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        matrix = TfidfVectorizer(stop_words="english").fit_transform([resume_text, job_description])
        text_similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except (ValueError, ImportError):
        text_similarity = 0.0
    skill_coverage = len(matched) / len(job_skills) if job_skills else 0.0
    score = round(100 * (0.75 * skill_coverage + 0.25 * text_similarity))
    return {
        "match_score": max(0, min(100, score)),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": matched,
        "missing_skills": missing,
        "text_similarity": round(text_similarity * 100, 1),
        "skill_coverage": round(skill_coverage * 100, 1),
    }
