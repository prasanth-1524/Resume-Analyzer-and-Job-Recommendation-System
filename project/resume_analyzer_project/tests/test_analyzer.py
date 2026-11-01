from analyzer import extract_skills, analyze_resume_against_job


def test_extract_skills_finds_known_terms():
    skills = extract_skills("I built a Flask app using Python, SQL and Git.")
    assert "python" in skills
    assert "flask" in skills
    assert "sql" in skills
    assert "git" in skills


def test_match_report_contains_missing_skills():
    report = analyze_resume_against_job(
        "Python developer with Flask and SQL experience",
        "Python, Flask, SQL, Docker and REST API required"
    )
    assert "python" in report["matched_skills"]
    assert "docker" in report["missing_skills"]
    assert 0 <= report["match_score"] <= 100
