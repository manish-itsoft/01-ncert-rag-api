from config.settings import settings
from config.logging_config import get_logger
from rag.retriever import get_retriever
from rag.generator import get_prompt, get_llm
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
 

logger = get_logger(__name__)

_chain = None

def format_docs(docs: list[Document]) -> str:
    """
    Format retrieved documents into a single context string.
    Includes source metadata for transparency.
    """
   
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        formatted.append(
            f"[{i}] Source: {source}\n{doc.page_content}"
        )
    response = "\n\n---\n\n".join(formatted)
    logger.debug(response)
    return response

def build_rag_chain(collection_name: str, top_k: int):
    """
    Build and return the two-step RAG chain using LCEL.

    Step 1 — Retrieve:  query → ChromaDB → top-K chunks
    Step 2 — Generate:  chunks + query + prompt → LLM → answer
    """

    global _chain
    if _chain is not None:
        return _chain
    
    retriever = get_retriever(collection_name, top_k)
    prompt    = get_prompt()
    llm       = get_llm()
    parser    = StrOutputParser()
    logger.debug(f"retriever: {retriever}")
    logger.debug(f"prompt: {prompt}")
    logger.debug(f"llm: {llm}")
    
    # logger.debug(f"parser type      : {type(parser).__name__}")
    # logger.debug(f"parser input type: {parser.InputType}")
    # logger.debug(f"parser output type: {parser.OutputType}")

    logger.info(f"RunnablePassthrough: {RunnablePassthrough}")

    # RunnableParallel runs both branches simultaneously:
    # - "context"  → retrieves docs and formats them
    # - "question" → passes the original question straight through
    retrieve_and_format = RunnableParallel({
        "context":  retriever | format_docs,
        "question": RunnablePassthrough(),
    })

    logger.debug(f"retrieve_and_format: {retrieve_and_format}")
    # Full LCEL chain: retrieve → prompt → LLM → parse
    _chain = retrieve_and_format | prompt | llm | parser

    return _chain