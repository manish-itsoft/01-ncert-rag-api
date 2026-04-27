# NCERT RAG API

A Retrieval-Augmented Generation (RAG) API built with Flask, LangChain, ChromaDB, and Ollama — designed to answer questions grounded in NCERT educational content.

---

## Architecture

The system follows a **two-step RAG pipeline**:

1. **Retrieve** — A user question is embedded and used to query a ChromaDB vector store, returning the top-K most semantically similar document chunks.
2. **Generate** — The retrieved chunks are injected into the system prompt as context, and a local Ollama LLM produces a grounded answer.

---

## Project Structure

```
├── main.py                   # Flask app entry point
├── api/
│   ├── routes.py             # API endpoint definitions
│   └── schemas.py            # Request/response dataclasses
├── rag/
│   ├── two_step_agent.py     # LangChain agent with dynamic prompt middleware
│   ├── retriever.py          # ChromaDB vector store + LangChain retriever
│   ├── generator.py          # Ollama LLM + system prompt builder
└── config/
    ├── settings.py           # All configuration constants
    └── logging_config.py     # Rotating file + console logger
```

---

## Configuration

All settings are centralised in `config/settings.py`:

| Config Class       | Key Settings                                              |
|--------------------|-----------------------------------------------------------|
| `EmbeddingConfig`  | `MODEL` — Ollama embedding model (`nomic-embed-text:v1.5`) |
| `VectorDBConfig`   | `PERSIST_DIR`, `COLLECTION` — ChromaDB path & collection  |
| `RetrievalConfig`  | `LLM_MODEL`, `TOP_K_DEFAULT`, `TOP_K_MIN`, `TOP_K_MAX`    |
| `FlaskAPIConfig`   | `HOST`, `PORT`, `DEBUG`, route prefixes & response strings |
| `LogConfig`        | `DIR` — log output directory                              |

---

## Getting Started

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) running locally with the following models pulled:
  ```bash
  ollama pull nomic-embed-text:v1.5
  ollama pull llama3.2:latest
  ```
- A pre-built ChromaDB vector store at the path specified in `VectorDBConfig.PERSIST_DIR`

### Installation

```bash
# Clone the repository
git clone https://github.com/manish-itsoft/01-ncert-rag-api.git
cd 01-ncert-rag-api

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the API

```bash
python main.py
```

The server starts at `http://0.0.0.0:80` by default.

---

## API Endpoints

### `GET /api/health`

Health check to confirm the API is running.

**Response**
```json
{ "status": "NCERT RAG API is running" }
```

---

### `POST /api/ask`

Ask a question against the NCERT document corpus.

**Request Body**
```json
{
  "question": "What is photosynthesis?",
  "top_k": 5
}
```

| Field      | Type    | Required | Description                                    |
|------------|---------|----------|------------------------------------------------|
| `question` | string  | ✅        | The question to answer                         |
| `top_k`    | integer | ❌        | Number of chunks to retrieve (default: `5`, range: `1–20`) |

**Response**
```json
{
  "question": "What is photosynthesis?",
  "answer": "Photosynthesis is the process by which..."
}
```
---

## How the RAG Agent Works

The `two_step_agent` uses a **LangChain agent** with a `dynamic_prompt` middleware:

1. Before every model call, `prompt_with_context` intercepts the request.
2. It extracts the user's question from the message history.
3. It calls the retriever to fetch the top-K relevant chunks from ChromaDB.
4. It injects those chunks into the system prompt.
5. The LLM generates an answer using only the provided context.

The agent is **cached as a singleton** after first initialisation to avoid reloading the model on every request.

---

## Logging

Logs are written to both the console and a rotating file under the configured `LOG_DIR`:

- **Format:** `timestamp | level | module | message`
- **Rotation:** 5 MB per file, up to 5 backups
- **Filename pattern:** `ingestion_YYYY-MM-DD.log`

---

## Tech Stack

| Component       | Library / Tool                        |
|-----------------|---------------------------------------|
| API Framework   | Flask                                 |
| LLM             | Ollama (`llama3.2`) via LangChain     |
| Embeddings      | Ollama (`nomic-embed-text`) via LangChain |
| Vector Store    | ChromaDB                              |
| RAG Orchestration | LangChain (Agent)            |
| Logging         | Python `logging` + `RotatingFileHandler` |