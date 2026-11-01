from openai import OpenAI

from .config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TOP_K
)

from .vector_store import search


SYSTEM_PROMPT = """
You are a document question-answering assistant.

Answer questions using only the supplied document context.

If the context does not contain enough information,
say that you do not have enough information in the
indexed documents.

Do not invent facts.

Do not invent citations.

Do not invent page numbers.

Keep answers clear and concise.
"""


# Create OpenAI client
client = None

if OPENAI_API_KEY:
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )


def answer_question(question):

    # Check API key
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    # Search ChromaDB
    results = search(
        question,
        TOP_K
    )

    # No relevant results
    if not results:

        return {
            "answer":
                "No relevant information was found.",

            "sources": []
        }

    context_blocks = []

    sources = []

    # Build context
    for index, result in enumerate(
        results,
        start=1
    ):

        metadata = result["metadata"]

        if metadata.get("page"):

            location = (
                f"page {metadata['page']}"
            )

        else:

            location = "document"

        context_blocks.append(
            f"[Source {index}] "
            f"{metadata['file']} "
            f"({location})\n"
            f"{result['text']}"
        )

        sources.append({

            "file":
                metadata.get("file"),

            "page":
                metadata.get("page"),

            "chunk":
                metadata.get("chunk"),

            "distance":
                result.get("distance")
        })

    # Combine retrieved chunks
    context = "\n\n".join(
        context_blocks
    )

    # User prompt
    prompt = f"""
Context:

{context}

Question:

{question}

Answer the question using only
the supplied context.

Mention relevant source files
or pages when useful.
"""

    # Call OpenAI
    response = client.chat.completions.create(

        model=OPENAI_MODEL,

        temperature=0,

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract answer
    answer = (
        response
        .choices[0]
        .message
        .content
    )

    return {

        "answer":
            answer,

        "sources":
            sources
    }