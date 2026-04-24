"""Application entry point for the Telegram sales bot."""

from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import load_settings
from app.database import Database
from app.handlers import setup_routers
from app.middlewares.rate_limit import RateLimitMiddleware
from app.services.ai_service import AIService
from app.services.faq_service import FAQService
from app.utils import setup_logging


async def set_commands(bot: Bot) -> None:
    """Register basic bot commands in Telegram."""

    commands = [
        BotCommand(command="start", description="Start / Перезапуск"),
        BotCommand(command="menu", description="Main menu / Главное меню"),
        BotCommand(command="language", description="Language / Язык"),
        BotCommand(command="cancel", description="Cancel / Отмена"),
        BotCommand(command="stats", description="Admin stats / Статистика"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    """Configure services and start polling."""

    settings = load_settings()
    setup_logging(settings.log_level)

    db = Database()
    await db.connect()
    await db.init_models()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.message.outer_middleware(RateLimitMiddleware(db=db, settings=settings))

    faq_service = FAQService(settings=settings)
    ai_service = AIService(settings=settings, db=db)

    setup_routers(
        dispatcher=dispatcher,
        settings=settings,
        db=db,
        ai_service=ai_service,
        faq_service=faq_service,
    )

    await set_commands(bot)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
