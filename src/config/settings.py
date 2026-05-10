from pathlib import Path
import os

class EmbeddingConfig:
    """Embedding model used during document ingestion."""
    MODEL = "nomic-embed-text:v1.5"
    
class VectorDBConfig:
    """ChromaDB vector store configuration."""
    TYPE = "chroma"
    PERSIST_DIR = Path(os.getenv("VECTOR_DB_PATH", "/data/vector_store"))
    COLLECTION = "ncert_ebooks"

class RetrievalConfig:
    """LLM + Retriever hyperparameters."""
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:latest")
    TOP_K_DEFAULT = int(os.getenv("TOP_K_DEFAULT", 5))
    TOP_K_MIN = int(os.getenv("TOP_K_MIN", 1))
    TOP_K_MAX = int(os.getenv("TOP_K_MAX", 20))

class LogConfig:
    """Directory for pipeline and API logs."""
    DIR = Path(os.getenv("LOG_DIR", "/app/logs"))

class FlaskAPIConfig:
    """Flask API runtime settings."""
    HOST =  "0.0.0.0"
    PORT = 80
    DEBUG = False

    ROUTE_PREFIX =  "/api"
    ROUTE_HEALTH = "/health"
    ROUTE_ASK = "/ask"
        
    RESPONSE_HEALTH =  "NCERT RAG API is running"
    RESPONSE_ASK_NO_DATA =  "Request body must be JSON"
    RESPONSE_ASK_NO_QUESTION = "Field 'question' is required and cannot be empty"
            
class Settings:
    log = LogConfig()
    flask_api = FlaskAPIConfig()
    embedding = EmbeddingConfig()
    vectordb = VectorDBConfig()
    retrieval = RetrievalConfig()
   
settings = Settings()