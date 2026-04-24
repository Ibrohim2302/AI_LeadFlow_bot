"""Handlers for AI-powered chat mode."""

from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import Settings
from app.database import Database
from app.handlers.common import mirror_message_to_admin, sync_user
from app.keyboards import build_main_menu
from app.services.ai_service import AIService
from app.services.faq_service import FAQService
from app.states import AIChat
from app.texts import t


logger = logging.getLogger(__name__)


async def _answer_question(
    *,
    message: Message,
    bot: Bot,
    state: FSMContext,
    settings: Settings,
    db: Database,
    ai_service: AIService,
    faq_service: FAQService,
) -> None:
    """Answer a user text with FAQ or OpenAI and keep AI mode active."""

    if message.from_user is None or message.text is None:
        return

    language = await sync_user(db, message.from_user)
    user_text = message.text.strip()

    await state.set_state(AIChat.active)
    await db.add_message(message.from_user.id, "user", user_text)
    await mirror_message_to_admin(bot, settings, message, language)

    faq_answer = faq_service.find_answer(user_text, language)
    if faq_answer is not None:
        await db.add_message(message.from_user.id, "assistant", faq_answer)
        await message.answer(faq_answer, reply_markup=build_main_menu(language))
        return

    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        ai_answer = await ai_service.generate_reply(message.from_user.id, language)
    except Exception:
        logger.exception("OpenAI request failed for user %s", message.from_user.id)
        ai_answer = t(language, "ai_error")

    await db.add_message(message.from_user.id, "assistant", ai_answer)
    await message.answer(ai_answer, reply_markup=build_main_menu(language))


def get_router(
    settings: Settings,
    db: Database,
    ai_service: AIService,
    faq_service: FAQService,
) -> Router:
    """Build the router that answers AI questions."""

    router = Router(name="ai_chat")

    @router.message(AIChat.active, F.text)
    async def ai_chat_handler(message: Message, bot: Bot, state: FSMContext) -> None:
        """Reply with FAQ or OpenAI while keeping short-term chat memory."""

        await _answer_question(
            message=message,
            bot=bot,
            state=state,
            settings=settings,
            db=db,
            ai_service=ai_service,
            faq_service=faq_service,
        )

    @router.message(F.text)
    async def fallback_handler(message: Message, bot: Bot, state: FSMContext) -> None:
        """Handle plain text outside explicit flows with a helpful prompt."""

        if message.from_user is None:
            return

        if await state.get_state() is not None:
            return

        await _answer_question(
            message=message,
            bot=bot,
            state=state,
            settings=settings,
            db=db,
            ai_service=ai_service,
            faq_service=faq_service,
        )

    return router
