from pathlib import Path

from pypdf import PdfReader


def extract_file(path):

    file_path = Path(path)

    extension = file_path.suffix.lower()

    # PDF files
    if extension == ".pdf":

        reader = PdfReader(
            str(file_path)
        )

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text()

            if text is None:
                text = ""

            pages.append(
                (
                    page_number,
                    text
                )
            )

        return pages

    # TXT and Markdown files
    if extension in {
        ".txt",
        ".md"
    }:

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        return [
            (None, text)
        ]

    # Unsupported files
    raise ValueError(
        "Supported files: PDF, TXT, MD"
    )