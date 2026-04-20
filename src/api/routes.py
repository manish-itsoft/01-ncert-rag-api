from flask import Blueprint, request, jsonify
from config.settings import settings
from config.logging_config import get_logger
# from rag.chain import build_rag_chain
from rag.two_step_agent import two_step_agent

logger = get_logger(__name__)

api_blueprint = Blueprint("api", __name__, url_prefix=settings.flask_api.ROUTE_PREFIX)

# Root health check
@api_blueprint.route(settings.flask_api.ROUTE_HEALTH, methods=["GET"])
def health_check():
    status_message = { "status": settings.flask_api.RESPONSE_HEALTH}
    logger.info(f"Health Check API Response: {status_message}")
    return jsonify(status_message), 200


@api_blueprint.route(settings.flask_api.ROUTE_ASK, methods=["POST"])
def ask():

    data = request.get_json(silent=False)
    if not data:
        response = jsonify({"error": settings.flask_api.RESPONSE_ASK_NO_DATA}), 400
        logger.info(f"Ask API Response: {response}")
        return response
    
    question = data.get("question", "").strip()
    if not question:
        response = {"error": settings.flask_api.RESPONSE_ASK_NO_QUESTION }
        logger.info(f"Ask API Response: {response}")
        return jsonify(response), 400
    
    top_k = data.get("top_k", settings.retrieval.TOP_K_DEFAULT)
    if not isinstance(top_k, int) or not (settings.retrieval.TOP_K_MIN <= top_k <= settings.retrieval.TOP_K_MAX):
        response = {"error": "'top_k' must be an integer between ${settings.retrieval.TOP_K_MIN} and ${settings.retrieval.TOP_K_MAX}"}
        logger.info(f"Ask API Response: {response}")
        return jsonify(response), 400
    
    answer = two_step_agent(question, top_k)
    logger.info(f"{settings.flask_api.ROUTE_ASK} API Response")
    response = {"question": question, "answer": answer}
    logger.info(response)
    return jsonify(response),200

    # retriever = get_retriever(settings.vectordb.COLLECTION)
    # retriever.search_kwargs["k"] = top_k
    # retrieved_docs = retriever.invoke(question)

    # --- Step 2: Generate answer ---
    # chain = build_rag_chain(settings.vectordb.COLLECTION, top_k)
    # answer = chain.invoke(question)
    # logger.info(f"Final Answer: {answer}")

    # # --- Build source list for UI display ---
    # sources = [
    #     {
    #         "content":  doc.page_content[:300],   # preview only
    #         "source":   doc.metadata.get("file_name", "unknown"),
    #         "page":     doc.metadata.get("page", None),
    #     }
    #     for doc in retrieved_docs
    # ]

    # return jsonify({
    #     "question":     question,
    #     # "answer":       answer,
    #     "sources":      sources,
    #     # "elapsed_sec":  elapsed,
    # }), 200

    # return jsonify({}), 200