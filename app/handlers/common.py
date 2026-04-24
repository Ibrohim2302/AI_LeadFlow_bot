"""Shared helper functions for handlers."""

from __future__ import annotations

import re
from html import escape

from aiogram import Bot
from aiogram.types import Message, User

from app.config import Settings
from app.database import Database
from app.texts import normalize_language, t


async def sync_user(db: Database, user: User, language: str | None = None) -> str:
    """Create or update the user record and return the active language."""

    stored_language = language or await db.get_user_language(user.id) or user.language_code
    normalized = normalize_language(stored_language)
    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        language=normalized,
    )
    return normalized


def normalize_phone(raw_phone: str) -> str | None:
    """Normalize a phone number to an international format."""

    digits = re.sub(r"[^\d+]", "", raw_phone.strip())
    if not digits:
        return None
    digits_only = re.sub(r"\D", "", digits)
    if len(digits_only) < 7 or len(digits_only) > 15:
        return None
    return f"+{digits_only}"


async def notify_admin(bot: Bot, settings: Settings, text: str) -> None:
    """Send a notification message to the configured admin chat."""

    await bot.send_message(settings.admin_id, text)


async def mirror_message_to_admin(
    bot: Bot,
    settings: Settings,
    message: Message,
    language: str,
) -> None:
    """Forward a compact user text summary to the admin when enabled."""

    if not settings.forward_all_messages:
        return
    if message.from_user is None or message.from_user.id == settings.admin_id:
        return
    if not message.text:
        return

    username = f"@{escape(message.from_user.username)}" if message.from_user.username else "not set"
    text = (
        f"<b>{t(language, 'new_message_admin')}</b>\n"
        f"Name: <b>{escape(message.from_user.full_name)}</b>\n"
        f"Username: <b>{username}</b>\n"
        f"User ID: <code>{message.from_user.id}</code>\n"
        f"Message: {escape(message.text)}"
    )
    await notify_admin(bot, settings, text)
