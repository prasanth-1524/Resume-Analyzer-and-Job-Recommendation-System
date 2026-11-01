import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)


OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)


EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)


CHROMA_DIR = os.getenv(
    "CHROMA_DIR",
    "./data/chroma"
)


COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "documents"
)


CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        "900"
    )
)


CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        "150"
    )
)


TOP_K = int(
    os.getenv(
        "TOP_K",
        "5"
    )
)