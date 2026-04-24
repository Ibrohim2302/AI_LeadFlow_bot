"""Formatting helpers and shared utility functions."""

from __future__ import annotations

import logging
from html import escape

from app.config import Settings
from app.texts import t


def setup_logging(log_level: str) -> None:
    """Configure simple production-friendly logging."""

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def format_services(settings: Settings, language: str) -> str:
    """Format the list of services for the user."""

    lines = [t(language, "services_header"), ""]
    for service in settings.services:
        lines.append(f"<b>{escape(service.localized_name(language))}</b> - {escape(service.price)}")
        lines.append(escape(service.localized_description(language)))
        lines.append("")
    lines.append(t(language, "services_footer"))
    return "\n".join(lines).strip()


def format_contact_info(settings: Settings, language: str) -> str:
    """Format business contact information in the selected language."""

    contact = settings.business_contact_ru if language == "ru" else settings.business_contact_en
    delivery_time = settings.delivery_time_ru if language == "ru" else settings.delivery_time_en
    contact_handle = settings.sales_username or "@your_username"
    return t(
        language,
        "contact_info",
        contact=escape(contact),
        contact_handle=escape(contact_handle),
        delivery_time=escape(delivery_time),
        price_from=escape(settings.price_from),
    )


def format_stats(stats: dict[str, int], language: str) -> str:
    """Build a localized stats message for the admin."""

    if language == "ru":
        return (
            f"{t(language, 'stats_title')}\n\n"
            f"Пользователи: <b>{stats['users']}</b>\n"
            f"Сообщения: <b>{stats['messages']}</b>\n"
            f"Все заявки: <b>{stats['leads']}</b>\n"
            f"Заказы: <b>{stats['orders']}</b>\n"
            f"Контактные заявки: <b>{stats['requests']}</b>"
        )
    return (
        f"{t(language, 'stats_title')}\n\n"
        f"Users: <b>{stats['users']}</b>\n"
        f"Messages: <b>{stats['messages']}</b>\n"
        f"All leads: <b>{stats['leads']}</b>\n"
        f"Orders: <b>{stats['orders']}</b>\n"
        f"Contact requests: <b>{stats['requests']}</b>"
    )


def format_admin_lead_message(
    *,
    language: str,
    lead_type: str,
    service_name: str | None,
    user_id: int,
    username: str | None,
    full_name: str,
    phone: str,
    request: str,
) -> str:
    """Format a lead notification for the admin."""

    user_link = f"@{escape(username)}" if username else "not set"

    if language == "ru":
        lead_label = "Новый заказ" if lead_type == "order" else "Новая заявка"
        service_line = f"\nУслуга: <b>{escape(service_name)}</b>" if service_name else ""
        return (
            f"<b>{lead_label}</b>{service_line}\n"
            f"Имя: <b>{escape(full_name)}</b>\n"
            f"Username: <b>{user_link}</b>\n"
            f"User ID: <code>{user_id}</code>\n"
            f"Телефон: <code>{escape(phone)}</code>\n"
            f"Запрос: {escape(request)}"
        )

    lead_label = "New order" if lead_type == "order" else "New lead"
    service_line = f"\nService: <b>{escape(service_name)}</b>" if service_name else ""
    return (
        f"<b>{lead_label}</b>{service_line}\n"
        f"Name: <b>{escape(full_name)}</b>\n"
        f"Username: <b>{user_link}</b>\n"
        f"User ID: <code>{user_id}</code>\n"
        f"Phone: <code>{escape(phone)}</code>\n"
        f"Request: {escape(request)}"
    )
