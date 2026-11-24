from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter


def create_documents(pdf_data: dict) -> list:
    """Convert extracted PDF pages into LlamaIndex documents."""

    documents = []

    for page in pdf_data["pages"]:
        if page["text"].strip():
            documents.append(
                Document(
                    text=page["text"],
                    metadata={
                        "file_name": pdf_data["file_name"],
                        "page_number": page["page_number"],
                    },
                )
            )

    return documents


def create_index(documents: list):
    """Create an in-memory vector index."""

    if not documents:
        raise ValueError("No documents available for indexing.")

    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=80,
    )

    return VectorStoreIndex.from_documents(
        documents,
        transformations=[splitter],
    )