# Makefile

OLLAMA_MODELS = qwen3.5:2b

.PHONY: models
models:
	@echo "Pulling Ollama models..."
	@for model in $(OLLAMA_MODELS); do \
		ollama pull $$model; \
	done
	@echo "✅ Done"