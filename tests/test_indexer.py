from src.ingestion.indexer import create_documents


def test_create_documents():
    pdf_data = {
        "file_name": "sample.pdf",
        "pages": [
            {"page_number": 1, "text": "This is page one."},
            {"page_number": 2, "text": "This is page two."},
            {"page_number": 3, "text": ""}
        ]
    }

    documents = create_documents(pdf_data)

    assert len(documents) == 2
    assert documents[0].metadata["page_number"] == 1
    assert documents[1].metadata["file_name"] == "sample.pdf"