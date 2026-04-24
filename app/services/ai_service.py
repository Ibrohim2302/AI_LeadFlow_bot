"""OpenAI service used for sales-style AI replies."""

from __future__ import annotations

from openai import AsyncOpenAI

from app.config import Settings
from app.database import Database
from app.texts import normalize_language


class AIService:
    """Generate OpenAI answers using stored chat history."""

    def __init__(self, settings: Settings, db: Database) -> None:
        """Create an async OpenAI client and store dependencies."""

        self.settings = settings
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate_reply(self, user_id: int, language: str) -> str:
        """Build a contextual AI answer from recent conversation history."""

        normalized_language = normalize_language(language)
        history = await self.db.get_recent_messages(
            user_id=user_id,
            limit=self.settings.ai_memory_messages,
        )

        response = await self.client.responses.create(
            model=self.settings.openai_model,
            instructions=self._build_system_prompt(normalized_language),
            input=[{"role": item["role"], "content": item["content"]} for item in history],
            max_output_tokens=350,
        )

        answer = (response.output_text or "").strip()
        return answer or self._fallback_answer(normalized_language)

    def _build_system_prompt(self, language: str) -> str:
        """Create a sales-focused system prompt in the selected language."""

        business_description = (
            self.settings.business_description_ru
            if language == "ru"
            else self.settings.business_description_en
        )
        business_contact = (
            self.settings.business_contact_ru
            if language == "ru"
            else self.settings.business_contact_en
        )
        service_lines = []
        for service in self.settings.services:
            service_lines.append(
                f"- {service.localized_name(language)} ({service.price}): "
                f"{service.localized_description(language)}"
            )
        service_block = "\n".join(service_lines)

        if language == "ru":
            return (
                "Ты профессиональный менеджер по продажам в Telegram для бизнеса.\n"
                f"Название бизнеса: {self.settings.business_name}\n"
                f"Описание бизнеса: {business_description}\n"
                f"Контакты: {business_contact}\n"
                "Твоя задача:\n"
                "- отвечать дружелюбно, уверенно и по делу;\n"
                "- помогать клиенту выбрать услугу;\n"
                "- подчеркивать выгоду: бот отвечает как живой менеджер и не пропускает клиентов;\n"
                "- мягко подводить к заявке или заказу;\n"
                "- писать на русском языке, если пользователь не просит иначе;\n"
                "- не выдумывать факты и цены сверх списка ниже.\n"
                "Список услуг:\n"
                f"{service_block}\n"
                f"Стартовая цена: {self.settings.price_from}\n"
                f"Срок запуска: {self.settings.delivery_time_ru}\n"
                "Если информации недостаточно, предложи оставить заявку для менеджера."
            )

        return (
            "You are a professional Telegram sales manager for a business.\n"
            f"Business name: {self.settings.business_name}\n"
            f"Business description: {business_description}\n"
            f"Contact details: {business_contact}\n"
            "Your job is to:\n"
            "- reply in a friendly, persuasive, and professional tone;\n"
            "- help the customer choose a service;\n"
            "- reinforce the value: the bot answers like a live manager and never misses customers;\n"
            "- gently move the conversation toward a lead or order;\n"
            "- answer in English unless the user clearly switches language;\n"
            "- never invent facts or prices outside the service list below.\n"
            "Service list:\n"
            f"{service_block}\n"
            f"Starter price: {self.settings.price_from}\n"
            f"Delivery time: {self.settings.delivery_time_en}\n"
            "If the request needs more details, invite the user to leave a lead."
        )

    def _fallback_answer(self, language: str) -> str:
        """Return a safe fallback if OpenAI returns an empty message."""

        if language == "ru":
            return "Спасибо за сообщение. Я помогу вам с выбором и могу передать ваш запрос менеджеру."
        return "Thank you for your message. I can help you choose a service and pass your request to the manager."
