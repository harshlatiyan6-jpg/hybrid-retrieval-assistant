import os
from dotenv import load_dotenv
from openai import OpenAI

from src.retrieval.qdrant_search import search_pdf

load_dotenv()


def retrieve_context(question, limit=5):
    results = search_pdf(question, limit=limit)

    contexts = []

    for result in results:
        if result.payload:
            contexts.append({
                "text": result.payload.get("text", ""),
                "page": result.payload.get("page"),
                "score": result.score,
            })

    return contexts


def build_rag_prompt(question, contexts):
    context_text = "\n\n".join(
        f"Page {item['page']}: {item['text']}"
        for item in contexts
    )

    return f"""
Answer using only the PDF context below.
If the answer is not present, say you could not find it in the PDF.

Context:
{context_text}

Question:
{question}
"""


def generate_answer(question, contexts):

    if not contexts:
        return "No relevant information found in the PDF."

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY missing in .env file")

    client = OpenAI(api_key=api_key)

    prompt = build_rag_prompt(question, contexts)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Answer questions using only the provided PDF context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content