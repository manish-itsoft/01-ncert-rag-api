from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)
_retriever = None

def get_retriever(collection_name: str, top_k: int = settings.retrieval.TOP_K_DEFAULT):
    """
    Load vectorstore and return a LangChain retriever.
    This is Step 1 of the two-step RAG chain.
    """
    global _retriever
    if _retriever is not None:
       logger.debug("Returning cached retriever")
       return _retriever

    logger.info(f"Initializing with {settings.embedding.MODEL} Embedding Model.")
    embeddings = OllamaEmbeddings(
        model=settings.embedding.MODEL,
        base_url=settings.retrieval.OLLAMA_HOST)

    logger.info(f"Loading Vectordb persist_directory {settings.vectordb.PERSIST_DIR} for collection_name {collection_name}")
    vectordb = Chroma(
        persist_directory=settings.vectordb.PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    # Add this debug check in retriever.py
    count = vectordb._collection.count()
    logger.debug(f"Collection '{collection_name}' has {count} docs")

    # Returns top-K most semantically similar chunks
    logger.info(f"Configure Retriever with similarity search and top_k {top_k}")
    _retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )

    return _retriever