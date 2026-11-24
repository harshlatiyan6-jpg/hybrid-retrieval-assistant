import pytest

from src.pdf_reader import chunk_text


def test_chunk_text_returns_chunks():
    text = " ".join(["hello"] * 2500)

    chunks = chunk_text(text, chunk_size=1000, overlap=150)

    assert len(chunks) == 3
    assert chunks[0]["chunk_id"] == 1
    assert chunks[1]["chunk_id"] == 2


def test_chunk_text_empty_input():
    assert chunk_text("") == []


def test_invalid_chunk_settings():
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=100, overlap=100)