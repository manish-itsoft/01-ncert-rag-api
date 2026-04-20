from pathlib import Path

class EmbeddingConfig:
    """Embedding model used during document ingestion."""
    MODEL = "nomic-embed-text:v1.5"
    
class VectorDBConfig:
    """ChromaDB vector store configuration."""
    TYPE = "chroma"
    PERSIST_DIR = Path("../../01-ncert-ebooks-rag-ingestion/.vector_store")
    COLLECTION = "ncert_ebooks"

class RetrievalConfig:
    """LLM + Retriever hyperparameters."""
    LLM_MODEL = "llama3.2:latest" #"qwen3.5:2b"
    TOP_K_DEFAULT = 5
    TOP_K_MIN = 1
    TOP_K_MAX = 20

class LogConfig:
    """Directory for pipeline and API logs."""
    DIR = Path("../logs/")

class FlaskAPIConfig:
    """Flask API runtime settings."""
    HOST =  "0.0.0.0"
    PORT = 80
    DEBUG = True

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