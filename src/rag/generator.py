# src/rag/generator.py

from langchain_ollama import ChatOllama
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

def get_system_prompt(docs_content: str) -> str:
    """
    Build the RAG prompt template.
    {context} is filled by the retriever output.
    {question} is filled by the user query.
    """
    
    system_prompt =  f"""You are a helpful assistant for NCERT educational content.
    Answer the question using ONLY the context provided below.
    If the answer is not in the context, say "I don't have enough information to answer this."
    Do not make up information.
    Context: 
    {docs_content}
    """

    #logger.debug(f"system_prompt: {system_prompt}")
    return system_prompt

def get_llm() -> ChatOllama:
    """Return the local Ollama LLM for generation."""
    logger.info(f"Configured LLM Model {settings.retrieval.LLM_MODEL}")
    return ChatOllama(
        model=settings.retrieval.LLM_MODEL,
        base_url=settings.retrieval.OLLAMA_HOST 
        # temperature=0,
        # extra_body={"think": False}
    )