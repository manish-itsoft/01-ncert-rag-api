FROM python:3.11-slim

ARG BUILD_DATE
ARG VERSION

# OCI LABELS for metadata
LABEL org.opencontainers.image.title="NCERT RAG API" \
      org.opencontainers.image.description="Python API for NCERT RAG" \
      org.opencontainers.image.version=$VERSION \
      org.opencontainers.image.authors="manish.itsoft" \
      org.opencontainers.image.source="https://github.com/manish-itsoft/01-ncert-rag-api.git" \
      org.opencontainers.image.created=$BUILD_DATE
      
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ .

# Create non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV OLLAMA_HOST=http://host.docker.internal:11434
ENV LOG_LEVEL=INFO

EXPOSE 80
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "--log-level", "${LOG_LEVEL}", "main:create_app()"]