"""Handlers for the main menu and action entry points."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import Settings
from app.database import Database
from app.handlers.common import sync_user
from app.keyboards import (
    build_cancel_keyboard,
    build_contact_keyboard,
    build_main_menu,
    build_services_keyboard,
)
from app.states import AIChat, LeadForm
from app.texts import CANCEL_LABELS, MENU_TEXT_TO_ACTION, t
from app.utils import format_contact_info, format_services


def get_router(settings: Settings, db: Database) -> Router:
    """Build the router for top-level menu navigation."""

    router = Router(name="menu")

    @router.message(Command("menu"))
    async def menu_command_handler(message: Message, state: FSMContext) -> None:
        """Clear the current flow and show the main menu."""

        if message.from_user is None:
            return

        language = await sync_user(db, message.from_user)
        await state.clear()
        await message.answer(t(language, "menu_shown"), reply_markup=build_main_menu(language))

    @router.message(Command("cancel"))
    @router.message(F.text.in_(tuple(CANCEL_LABELS)))
    async def cancel_handler(message: Message, state: FSMContext) -> None:
        """Cancel the active flow and return the user to the menu."""

        if message.from_user is None:
            return

        language = await sync_user(db, message.from_user)
        await state.clear()
        await message.answer(t(language, "cancelled"), reply_markup=build_main_menu(language))

    @router.message(F.text.in_(tuple(MENU_TEXT_TO_ACTION.keys())))
    async def menu_buttons_handler(message: Message, state: FSMContext) -> None:
        """Open the menu section selected by the user."""

        if message.from_user is None or message.text is None:
            return

        language = await sync_user(db, message.from_user)
        action = MENU_TEXT_TO_ACTION[message.text]

        if action != "ask_ai":
            await state.clear()

        if action == "services":
            await message.answer(
                format_services(settings, language),
                reply_markup=build_services_keyboard(settings, language),
            )
            return

        if action == "order":
            await message.answer(
                t(language, "order_choose_service"),
                reply_markup=build_services_keyboard(settings, language),
            )
            return

        if action == "contact":
            await message.answer(
                format_contact_info(settings, language),
                reply_markup=build_contact_keyboard(settings, language),
            )
            return

        await state.set_state(AIChat.active)
        await message.answer(
            t(language, "ask_ai_intro"),
            reply_markup=build_main_menu(language),
        )

    @router.callback_query(F.data.startswith("order:"))
    async def order_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
        """Start the order flow after the user picks a service."""

        if callback.from_user is None or callback.message is None or callback.data is None:
            return

        language = await sync_user(db, callback.from_user)
        service_code = callback.data.split(":", maxsplit=1)[1]
        service = settings.get_service(service_code)

        if service is None:
            await callback.answer(t(language, "service_not_found"), show_alert=True)
            return

        await state.clear()
        await state.update_data(lead_type="order", service_code=service_code)
        await state.set_state(LeadForm.waiting_name)

        await callback.answer()
        await callback.message.answer(
            f"{t(language, 'service_selected', service=service.localized_name(language))}\n"
            f"{t(language, 'lead_name')}",
            reply_markup=build_cancel_keyboard(language),
        )

    @router.callback_query(F.data == "lead:start")
    async def lead_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
        """Start a generic contact request flow."""

        if callback.from_user is None or callback.message is None:
            return

        language = await sync_user(db, callback.from_user)
        await state.clear()
        await state.update_data(lead_type="lead", service_code=None)
        await state.set_state(LeadForm.waiting_name)

        await callback.answer()
        await callback.message.answer(
            t(language, "lead_name"),
            reply_markup=build_cancel_keyboard(language),
        )

    return router
