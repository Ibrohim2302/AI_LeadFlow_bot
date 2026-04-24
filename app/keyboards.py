"""Keyboard builders for reply and inline menus."""

from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import Settings
from app.texts import menu_label, t


def build_language_keyboard() -> InlineKeyboardMarkup:
    """Build an inline keyboard for language selection."""

    builder = InlineKeyboardBuilder()
    builder.button(text="Русский", callback_data="lang:ru")
    builder.button(text="English", callback_data="lang:en")
    builder.adjust(2)
    return builder.as_markup()


def build_main_menu(language: str) -> ReplyKeyboardMarkup:
    """Build the main reply keyboard required by the project."""

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=menu_label("services", language)),
                KeyboardButton(text=menu_label("ask_ai", language)),
            ],
            [KeyboardButton(text=menu_label("contact", language))],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def build_cancel_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Build a small keyboard with only a cancel button."""

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(language, "cancel"))]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_phone_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Build a keyboard that asks Telegram for the user's phone number."""

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(language, "share_phone"), request_contact=True)],
            [KeyboardButton(text=t(language, "cancel"))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_services_keyboard(settings: Settings, language: str) -> InlineKeyboardMarkup:
    """Build an inline keyboard with order buttons for each service."""

    builder = InlineKeyboardBuilder()
    for service in settings.services:
        builder.button(
            text=f"{service.localized_name(language)} - {service.price}",
            callback_data=f"order:{service.code}",
        )
    builder.adjust(1)
    return builder.as_markup()


def build_contact_keyboard(settings: Settings, language: str) -> InlineKeyboardMarkup:
    """Build an inline keyboard for starting a contact request."""

    builder = InlineKeyboardBuilder()
    builder.button(text=t(language, "contact_button"), callback_data="lead:start")
    sales_handle = settings.sales_username.lstrip("@")
    if sales_handle:
        builder.button(
            text=t(language, "contact_direct_button"),
            url=f"https://t.me/{sales_handle}",
        )
        builder.adjust(1)
    return builder.as_markup()
