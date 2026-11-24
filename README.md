# Hybrid Retrieval Assistant

An AI-powered document question-answering system built using Hybrid Search and Retrieval-Augmented Generation (RAG).

## Overview

The Hybrid Retrieval Assistant is designed to retrieve relevant information from documents using a combination of semantic search and keyword-based retrieval. It uses retrieved context to generate relevant answers to user queries.

## Key Features

- Hybrid Retrieval using semantic and keyword search
- Vector search with Qdrant
- Keyword retrieval using BM25
- Retrieval-Augmented Generation (RAG)
- Neo4j integration for knowledge graph capabilities
- Python-based architecture

## Technology Stack

- Python 3.11
- LlamaIndex
- Qdrant
- BM25
- Neo4j
- OpenAI-compatible LLM integration

## Project Structure

```text
hybrid-retrieval-assistant/
│
├── src/
│   ├── main.py
│   └── retrieval/
│
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/harshlatiyan6-jpg/hybrid-retrieval-assistant.git
```

2. Open the project directory:

```bash
cd hybrid-retrieval-assistant
```

3. Create a virtual environment:

```bash
python3.11 -m venv .venv
```

4. Activate it:

```bash
source .venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file using `.env.example` and configure the required service credentials and settings.

Never upload API keys, passwords, or private credentials to GitHub.

## Running the Project

Run the application using the entry point configured in the project:

```bash
python src/main.py
```

## Testing

Run the test suite:

```bash
pytest
```

## Learning Outcomes

- Understanding Hybrid Search
- Working with vector databases
- Implementing RAG workflows
- Exploring knowledge graph integration
- Building Python-based AI applications

## Future Improvements

- Improve retrieval accuracy
- Add more document formats
- Enhance response quality
- Improve the user interface
- Add evaluation metrics

## Author

**Harsh Choudhary**

GitHub: https://github.com/harshlatiyan6-jpg

---

*This project is developed as part of my learning and exploration of AI, information retrieval, and Retrieval-Augmented Generation.*
