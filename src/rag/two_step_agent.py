from rag.retriever import get_retriever
from rag.generator import get_system_prompt, get_llm
from config.settings import settings
from config.logging_config import get_logger
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from dataclasses import dataclass
from langchain.messages import HumanMessage

logger = get_logger(__name__)

_agent = None

# Step 1: Define context schema
# To pass top_k and any other config at invoke time
@dataclass
class RAGContext:
    top_k: int = settings.retrieval.TOP_K_DEFAULT

# Step 2: Define dynamic_prompt middleware 
@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """
    Middleware that runs before every model call.
    Retrieves relevant docs from ChromaDB and injects them
    into the system prompt as context.
    """

    # Extract the user's question from the last human message
    messages  = request.state.get("messages", [])
    question  = ""
    for msg in reversed(messages):
        if hasattr(msg, "type") and msg.type == "human":
            question = msg.content
            break

    # Extract top_k from runtime context (passed at invoke time)
    top_k = request.runtime.context.top_k

    logger.debug(f"prompt_with_context → question='{question[:60]}' top_k={top_k}")
    
    retriever = get_retriever(settings.vectordb.COLLECTION, top_k)
    retriever.search_kwargs["k"] = top_k
    retrieved_docs = retriever.invoke(question) if question else []
    logger.debug(f"Retrieved {len(retrieved_docs)} docs for context")
    logger.debug(f"retrieved_docs: {retrieved_docs}")

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    system_prompt = get_system_prompt(docs_content)

    return system_prompt

# Step 3: Build the agent
def get_agent():
    global _agent
    if _agent is not None:
        logger.debug("Returning cached _agent")
        return _agent

    model = get_llm()
    logger.info(f"Building agent with model: {settings.retrieval.LLM_MODEL}")

    _agent = create_agent(
        model, 
        tools=[], 
        middleware=[prompt_with_context],
        context_schema=RAGContext
    )

    return _agent

# Step 4: Invoke function
def two_step_agent(question: str, top_k: int):

    agent = get_agent()
    logger.info(f"two_step_agent invoked — question='{question[:60]}' top_k={top_k}")
    
    response = agent.invoke(
        {
            "messages": [HumanMessage(content=question)]
        },
        context=RAGContext(top_k=top_k)
    )
    
    logger.debug("two_step_agent response")
    logger.debug(response)    

    # Extract the final text answer from the response messages
    last_message = response["messages"][-1]
    return last_message.content
    
