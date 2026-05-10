# src/api/schemas.py

from dataclasses import dataclass
from config.settings import settings

@dataclass
class QuestionRequest:
    question: str
    top_k: int = settings.TOP_K

@dataclass
class SourceDocument:
    content: str
    source: str
    page: int | None

@dataclass
class AnswerResponse:
    question: str
    answer: str
    sources: list[SourceDocument]