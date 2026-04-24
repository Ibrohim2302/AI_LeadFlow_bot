"""Configuration and editable business content for the bot."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class ServiceItem:
    """Describe one service that can be shown and ordered in the bot."""

    code: str
    name_ru: str
    name_en: str
    price: str
    description_ru: str
    description_en: str

    def localized_name(self, language: str) -> str:
        """Return the service name in the requested language."""

        return self.name_ru if language == "ru" else self.name_en

    def localized_description(self, language: str) -> str:
        """Return the service description in the requested language."""

        return self.description_ru if language == "ru" else self.description_en


@dataclass(frozen=True, slots=True)
class FAQItem:
    """Store a predefined FAQ answer and matching keywords."""

    keywords: tuple[str, ...]
    answer_ru: str
    answer_en: str

    def localized_answer(self, language: str, **kwargs: str) -> str:
        """Return the FAQ answer in the requested language."""

        template = self.answer_ru if language == "ru" else self.answer_en
        return template.format(**kwargs)


@dataclass(frozen=True, slots=True)
class Settings:
    """Keep all runtime settings in one immutable object."""

    bot_token: str
    openai_api_key: str
    openai_model: str
    admin_id: int
    business_name: str
    business_description_ru: str
    business_description_en: str
    business_contact_ru: str
    business_contact_en: str
    sales_username: str
    price_from: str
    delivery_time_ru: str
    delivery_time_en: str
    log_level: str
    rate_limit_messages: int
    rate_limit_window_seconds: int
    ai_memory_messages: int
    forward_all_messages: bool
    services: tuple[ServiceItem, ...]
    faqs: tuple[FAQItem, ...]

    def get_service(self, code: str | None) -> ServiceItem | None:
        """Find a service by its internal code."""

        if not code:
            return None
        for service in self.services:
            if service.code == code:
                return service
        return None


def _require_env(name: str) -> str:
    """Read a required environment variable and fail with a clear message."""

    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Environment variable {name} is required.")
    return value


def _read_bool(name: str, default: bool) -> bool:
    """Convert a textual environment variable to a boolean value."""

    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def default_services() -> tuple[ServiceItem, ...]:
    """Return starter services that can be sold to different businesses."""

    return (
        ServiceItem(
            code="full_ai_sales_bot",
            name_ru="Полный AI-бот для продаж",
            name_en="Full AI Sales Bot",
            price="$150",
            description_ru="Полноценный бот, который отвечает клиентам как менеджер, собирает заявки и помогает доводить диалог до покупки.",
            description_en="A complete bot that answers customers like a manager, captures leads, and helps move the chat toward a sale.",
        ),
        ServiceItem(
            code="faq_auto_replies",
            name_ru="FAQ + автоответы",
            name_en="FAQ + Auto Replies",
            price="$70",
            description_ru="Быстрые автоответы на частые вопросы, чтобы не тратить время менеджера на однотипные переписки.",
            description_en="Fast automated answers to common questions so the manager does not waste time on repetitive chats.",
        ),
        ServiceItem(
            code="order_capture",
            name_ru="Приём заказов и заявок",
            name_en="Order and Lead Capture",
            price="$90",
            description_ru="Сбор имени, телефона и запроса с отправкой заявки владельцу или менеджеру в Telegram.",
            description_en="Collects name, phone, and request and sends the lead directly to the owner or manager in Telegram.",
        ),
        ServiceItem(
            code="booking_bot",
            name_ru="Запись клиентов",
            name_en="Client Booking Bot",
            price="$100",
            description_ru="Подходит для салонов, услуг и консультаций: помогает записывать клиентов без пропусков.",
            description_en="Perfect for salons, services, and consultations: helps book customers without missing requests.",
        ),
    )


def default_faqs() -> tuple[FAQItem, ...]:
    """Return a small FAQ base to reduce OpenAI costs."""

    return (
        FAQItem(
            keywords=("price", "pricing", "cost", "сколько", "цена", "стоимость"),
            answer_ru="Стартовая цена от {price_from}. Точная стоимость зависит от набора функций. Напишите, что именно нужно, и я помогу подобрать лучший вариант.",
            answer_en="The starter price is from {price_from}. The exact cost depends on the feature set. Tell me what you need, and I will help you choose the best option.",
        ),
        FAQItem(
            keywords=("time", "deadline", "delivery", "срок", "когда", "быстро"),
            answer_ru="Обычно базовый запуск занимает {delivery_time}. Для точной оценки лучше оставить заявку, и я скажу по сроку честно.",
            answer_en="A basic setup usually takes {delivery_time}. For an exact estimate, it is best to leave a request and I will give you a realistic timeline.",
        ),
        FAQItem(
            keywords=("support", "help", "maintenance", "поддержка", "сопровождение"),
            answer_ru="Да, мы можем подключить сопровождение, обновления и доработки после запуска проекта.",
            answer_en="Yes, we can provide support, updates, and improvements after the project goes live.",
        ),
        FAQItem(
            keywords=("discount", "offer", "sale", "скидка", "акция", "спецпредложение"),
            answer_ru="Для постоянных клиентов и пакетов услуг мы можем предложить выгодные условия. Напишите, что вас интересует.",
            answer_en="We can offer better terms for repeat clients and service bundles. Tell me what you are interested in.",
        ),
    )


def load_settings() -> Settings:
    """Load environment variables and return validated settings."""

    load_dotenv()

    return Settings(
        bot_token=_require_env("BOT_TOKEN"),
        openai_api_key=_require_env("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip(),
        admin_id=int(_require_env("ADMIN_ID")),
        business_name=os.getenv("BUSINESS_NAME", "Demo Sales Studio").strip(),
        business_description_ru=os.getenv(
            "BUSINESS_DESCRIPTION_RU",
            "Мы автоматизируем продажи, принимаем заявки и помогаем бизнесу общаться с клиентами 24/7.",
        ).strip(),
        business_description_en=os.getenv(
            "BUSINESS_DESCRIPTION_EN",
            "We build Telegram AI bots that answer like a live manager and never miss customers.",
        ).strip(),
        business_contact_ru=os.getenv(
            "BUSINESS_CONTACT_RU",
            "Telegram: @your_username | Телефон: +7 999 123-45-67 | Email: sales@example.com",
        ).strip(),
        business_contact_en=os.getenv(
            "BUSINESS_CONTACT_EN",
            "Telegram: @your_username | Phone: +1 555 123 4567 | Email: sales@example.com",
        ).strip(),
        sales_username=os.getenv("SALES_USERNAME", "@your_username").strip(),
        price_from=os.getenv("PRICE_FROM", "$50").strip(),
        delivery_time_ru=os.getenv("DELIVERY_TIME_RU", "2-3 дня").strip(),
        delivery_time_en=os.getenv("DELIVERY_TIME_EN", "2-3 days").strip(),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
        rate_limit_messages=int(os.getenv("RATE_LIMIT_MESSAGES", "6")),
        rate_limit_window_seconds=int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "15")),
        ai_memory_messages=int(os.getenv("AI_MEMORY_MESSAGES", "10")),
        forward_all_messages=_read_bool("FORWARD_ALL_MESSAGES", True),
        services=default_services(),
        faqs=default_faqs(),
    )
