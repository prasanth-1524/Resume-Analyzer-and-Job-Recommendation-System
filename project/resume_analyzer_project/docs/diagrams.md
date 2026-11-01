# System Diagrams

These Mermaid diagrams can be pasted into a Mermaid-compatible editor or included as figures in the report.

## 1. System architecture
```mermaid
flowchart TD
    U[User / Browser] --> UI[HTML + Bootstrap UI]
    UI --> F[Flask Routes]
    F --> A[Resume Analyzer]
    A --> P[PDF / DOCX Text Extractor]
    A --> N[Skill Extraction + TF-IDF]
    F --> D[(SQLite Database)]
    F --> S[Local Upload Storage]
    N --> F
    F --> UI
```

## 2. Resume analysis flow
```mermaid
flowchart TD
    A[Start] --> B[User logs in]
    B --> C[Upload PDF or DOCX]
    C --> D{Allowed extension and size?}
    D -- No --> E[Show validation error]
    D -- Yes --> F[Extract document text]
    F --> G[Detect resume skills]
    G --> H[Compare against each job description]
    H --> I[Calculate skill coverage and TF-IDF similarity]
    I --> J[Rank jobs and list skill gaps]
    J --> K[User reviews or saves analysis]
    K --> L[End]
```

## 3. Entity relationships
```mermaid
erDiagram
    USERS ||--o{ RESUMES : uploads
    RESUMES ||--o{ RESUME_SKILLS : contains
    SKILLS ||--o{ RESUME_SKILLS : labels
    JOBS ||--o{ JOB_SKILLS : requires
    SKILLS ||--o{ JOB_SKILLS : labels
    USERS ||--o{ ANALYSIS_RESULTS : owns
    RESUMES ||--o{ ANALYSIS_RESULTS : analyzed
    JOBS ||--o{ ANALYSIS_RESULTS : compared_with
    USERS ||--o{ SAVED_JOBS : saves
    JOBS ||--o{ SAVED_JOBS : saved_by
```

## 4. Use-case overview
```mermaid
flowchart LR
    User((Student))
    User --> R[Register / Login]
    User --> U[Upload Resume]
    User --> A[Analyze Skills]
    User --> J[Browse Recommended Jobs]
    User --> G[View Skill Gaps]
    User --> S[Save Jobs]
    User --> H[View Analysis History]
```
