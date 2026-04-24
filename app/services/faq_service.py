"""FAQ service for inexpensive predefined answers."""

from __future__ import annotations

import re

from app.config import Settings
from app.texts import normalize_language


class FAQService:
    """Find matching FAQ answers before calling OpenAI."""

    def __init__(self, settings: Settings) -> None:
        """Store settings with FAQ content."""

        self.settings = settings

    def find_answer(self, question: str, language: str) -> str | None:
        """Return a predefined FAQ answer if a good keyword match is found."""

        normalized_question = self._normalize(question)
        best_score = 0
        best_answer: str | None = None
        localized_language = normalize_language(language)
        delivery_time = (
            self.settings.delivery_time_ru
            if localized_language == "ru"
            else self.settings.delivery_time_en
        )

        for item in self.settings.faqs:
            score = sum(1 for keyword in item.keywords if keyword in normalized_question)
            if score > best_score:
                best_score = score
                best_answer = item.localized_answer(
                    localized_language,
                    price_from=self.settings.price_from,
                    delivery_time=delivery_time,
                )

        if best_score == 0:
            return None
        return best_answer

    def _normalize(self, question: str) -> str:
        """Normalize the question text for rough keyword matching."""

        cleaned = re.sub(r"[^a-zA-Zа-яА-Я0-9\s]", " ", question.lower())
        return " ".join(cleaned.split())
