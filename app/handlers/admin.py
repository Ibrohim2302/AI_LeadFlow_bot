"""Admin-only handlers."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import Settings
from app.database import Database
from app.handlers.common import sync_user
from app.texts import t
from app.utils import format_stats


def get_router(settings: Settings, db: Database) -> Router:
    """Build the router with simple admin commands."""

    router = Router(name="admin")

    @router.message(Command("stats"))
    async def stats_handler(message: Message) -> None:
        """Show bot statistics to the configured admin."""

        if message.from_user is None:
            return

        language = await sync_user(db, message.from_user)
        if message.from_user.id != settings.admin_id:
            await message.answer(t(language, "admin_only"))
            return

        stats = await db.get_stats()
        await message.answer(format_stats(stats, language))

    return router
