"""FSM handlers for leads and orders."""

from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import Settings
from app.database import Database
from app.handlers.common import normalize_phone, notify_admin, sync_user
from app.keyboards import build_cancel_keyboard, build_main_menu, build_phone_keyboard
from app.states import LeadForm
from app.texts import t
from app.utils import format_admin_lead_message


logger = logging.getLogger(__name__)


def get_router(settings: Settings, db: Database) -> Router:
    """Build the router that collects lead form fields."""

    router = Router(name="forms")

    @router.message(LeadForm.waiting_name, F.text)
    async def lead_name_handler(message: Message, state: FSMContext) -> None:
        """Save the lead name and ask for a phone number."""

        if message.from_user is None or message.text is None:
            return

        language = await sync_user(db, message.from_user)
        await state.update_data(name=message.text.strip())
        await state.set_state(LeadForm.waiting_phone)
        await message.answer(
            t(language, "lead_phone"),
            reply_markup=build_phone_keyboard(language),
        )

    @router.message(LeadForm.waiting_phone, F.contact)
    async def lead_contact_handler(message: Message, state: FSMContext) -> None:
        """Save the shared Telegram contact and ask for the request text."""

        if message.from_user is None or message.contact is None:
            return

        language = await sync_user(db, message.from_user)
        phone = normalize_phone(message.contact.phone_number)
        if phone is None:
            await message.answer(t(language, "invalid_phone"), reply_markup=build_phone_keyboard(language))
            return

        await state.update_data(phone=phone)
        await state.set_state(LeadForm.waiting_request)
        await message.answer(
            t(language, "lead_request"),
            reply_markup=build_cancel_keyboard(language),
        )

    @router.message(LeadForm.waiting_phone, F.text)
    async def lead_phone_handler(message: Message, state: FSMContext) -> None:
        """Validate a manually entered phone number and continue the flow."""

        if message.from_user is None or message.text is None:
            return

        language = await sync_user(db, message.from_user)
        phone = normalize_phone(message.text)
        if phone is None:
            await message.answer(t(language, "invalid_phone"), reply_markup=build_phone_keyboard(language))
            return

        await state.update_data(phone=phone)
        await state.set_state(LeadForm.waiting_request)
        await message.answer(
            t(language, "lead_request"),
            reply_markup=build_cancel_keyboard(language),
        )

    @router.message(LeadForm.waiting_request, F.text)
    async def lead_request_handler(
        message: Message,
        state: FSMContext,
        bot: Bot,
    ) -> None:
        """Finish the flow, save the lead, and notify the admin."""

        if message.from_user is None or message.text is None:
            return

        language = await sync_user(db, message.from_user)
        data = await state.get_data()

        service = settings.get_service(data.get("service_code"))
        service_name = service.localized_name(language) if service else None
        lead_type = data.get("lead_type", "lead")
        name = data.get("name", message.from_user.full_name)
        phone = data.get("phone")
        request_text = message.text.strip()

        if phone is None:
            logger.warning("Lead flow finished without phone for user %s", message.from_user.id)
            await message.answer(t(language, "invalid_phone"), reply_markup=build_phone_keyboard(language))
            await state.set_state(LeadForm.waiting_phone)
            return

        await db.add_lead(
            user_id=message.from_user.id,
            lead_type=lead_type,
            service_code=data.get("service_code"),
            service_name=service_name,
            name=name,
            phone=phone,
            request=request_text,
        )

        admin_language = "ru"
        await notify_admin(
            bot,
            settings,
            format_admin_lead_message(
                language=admin_language,
                lead_type=lead_type,
                service_name=service_name,
                user_id=message.from_user.id,
                username=message.from_user.username,
                full_name=name,
                phone=phone,
                request=request_text,
            ),
        )

        await state.clear()
        await message.answer(
            t(language, "lead_success"),
            reply_markup=build_main_menu(language),
        )

    return router
