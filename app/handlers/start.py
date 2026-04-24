"""Handlers for bot start and language selection."""

from __future__ import annotations

from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import Settings
from app.database import Database
from app.handlers.common import sync_user
from app.keyboards import build_language_keyboard, build_main_menu
from app.texts import normalize_language, t


def get_router(settings: Settings, db: Database) -> Router:
    """Build the router responsible for onboarding and language choice."""

    router = Router(name="start")

    @router.message(CommandStart())
    async def start_handler(message: Message, state: FSMContext) -> None:
        """Register the user, reset state, and show language + main menu."""

        if message.from_user is None:
            return

        await state.clear()
        language = await sync_user(db, message.from_user)

        await message.answer(
            t(language, "choose_language"),
            reply_markup=build_language_keyboard(),
        )
        await message.answer(
            t(
                language,
                "welcome",
                business_name=escape(settings.business_name),
                description=(
                    escape(settings.business_description_ru)
                    if language == "ru"
                    else escape(settings.business_description_en)
                ),
            ),
            reply_markup=build_main_menu(language),
        )

    @router.message(Command("language"))
    async def language_command_handler(message: Message) -> None:
        """Show the language picker on demand."""

        if message.from_user is None:
            return

        language = await sync_user(db, message.from_user)
        await message.answer(
            t(language, "choose_language"),
            reply_markup=build_language_keyboard(),
        )

    @router.callback_query(F.data.startswith("lang:"))
    async def language_callback_handler(
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        """Save the chosen language and refresh the main menu."""

        if callback.from_user is None or callback.message is None or callback.data is None:
            return

        await state.clear()
        language = normalize_language(callback.data.split(":", maxsplit=1)[1])
        await sync_user(db, callback.from_user, language)
        await db.update_user_language(callback.from_user.id, language)

        await callback.answer(t(language, "language_saved"))
        await callback.message.answer(
            t(
                language,
                "welcome",
                business_name=escape(settings.business_name),
                description=(
                    escape(settings.business_description_ru)
                    if language == "ru"
                    else escape(settings.business_description_en)
                ),
            ),
            reply_markup=build_main_menu(language),
        )

    return router
