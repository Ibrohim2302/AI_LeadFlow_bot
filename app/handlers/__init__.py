"""Router setup for the Telegram bot."""

from __future__ import annotations

from aiogram import Dispatcher

from app.config import Settings
from app.database import Database
from app.handlers.admin import get_router as get_admin_router
from app.handlers.ai_chat import get_router as get_ai_router
from app.handlers.errors import get_router as get_errors_router
from app.handlers.forms import get_router as get_forms_router
from app.handlers.menu import get_router as get_menu_router
from app.handlers.start import get_router as get_start_router
from app.services.ai_service import AIService
from app.services.faq_service import FAQService


def setup_routers(
    dispatcher: Dispatcher,
    settings: Settings,
    db: Database,
    ai_service: AIService,
    faq_service: FAQService,
) -> None:
    """Attach all application routers to the dispatcher in a safe order."""

    dispatcher.include_router(get_errors_router())
    dispatcher.include_router(get_start_router(settings=settings, db=db))
    dispatcher.include_router(get_menu_router(settings=settings, db=db))
    dispatcher.include_router(get_admin_router(settings=settings, db=db))
    dispatcher.include_router(get_forms_router(settings=settings, db=db))
    dispatcher.include_router(
        get_ai_router(
            settings=settings,
            db=db,
            ai_service=ai_service,
            faq_service=faq_service,
        )
    )
