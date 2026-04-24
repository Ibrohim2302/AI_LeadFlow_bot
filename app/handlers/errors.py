"""Global error handler."""

from __future__ import annotations

import logging

from aiogram import Router
from aiogram.types import CallbackQuery, ErrorEvent, Message

from app.texts import normalize_language, t


logger = logging.getLogger(__name__)


def get_router() -> Router:
    """Build a router that logs and gracefully handles unexpected errors."""

    router = Router(name="errors")

    @router.errors()
    async def error_handler(event: ErrorEvent) -> bool:
        """Log the exception and try to notify the affected user."""

        logger.error(
            "Unhandled bot error",
            exc_info=(type(event.exception), event.exception, event.exception.__traceback__),
        )

        message: Message | None = getattr(event.update, "message", None)
        callback_query: CallbackQuery | None = getattr(event.update, "callback_query", None)

        target_message = message or (callback_query.message if callback_query else None)
        from_user = message.from_user if message else (callback_query.from_user if callback_query else None)

        if target_message is not None:
            language = normalize_language(from_user.language_code if from_user else None)
            await target_message.answer(t(language, "unexpected_error"))

        return True

    return router
