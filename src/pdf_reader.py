from pathlib import Path
from pypdf import PdfReader


def read_pdf(file_path: str) -> dict:
    """Extract text and metadata from a PDF file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    reader = PdfReader(str(path))

    if reader.is_encrypted:
        raise ValueError("This PDF is password protected.")

    pages = []
    full_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page_number": page_number,
            "text": text.strip()
        })

        if text.strip():
            full_text.append(text.strip())

    metadata = reader.metadata

    return {
        "file_name": path.name,
        "total_pages": len(reader.pages),
        "title": metadata.title if metadata else None,
        "author": metadata.author if metadata else None,
        "pages": pages,
        "full_text": "\n\n".join(full_text)
    }


def chunk_text(text: str, chunk_size: int = 1000,
               overlap: int = 150) -> list:
    """Split document text into overlapping chunks."""

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap.")

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunks.append({
            "chunk_id": len(chunks) + 1,
            "text": " ".join(words[start:end])
        })

        if end == len(words):
            break

        start = end - overlap

    return chunks