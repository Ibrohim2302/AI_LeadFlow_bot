"""Simple anti-spam middleware for Telegram messages."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.config import Settings
from app.database import Database
from app.texts import normalize_language, t


class RateLimitMiddleware(BaseMiddleware):
    """Limit how many messages each user can send in a short time."""

    def __init__(self, db: Database, settings: Settings) -> None:
        """Store dependencies and prepare in-memory user buckets."""

        self.db = db
        self.settings = settings
        self.timestamps: defaultdict[int, deque[float]] = defaultdict(deque)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Block the event when the user exceeds the configured limit."""

        if not isinstance(event, Message) or event.from_user is None:
            return await handler(event, data)

        if event.from_user.id == self.settings.admin_id:
            return await handler(event, data)

        user_id = event.from_user.id
        bucket = self.timestamps[user_id]
        now = time.monotonic()
        window_start = now - self.settings.rate_limit_window_seconds

        while bucket and bucket[0] < window_start:
            bucket.popleft()

        if len(bucket) >= self.settings.rate_limit_messages:
            stored_language = await self.db.get_user_language(user_id)
            language = normalize_language(stored_language or event.from_user.language_code)
            await event.answer(
                t(
                    language,
                    "spam_warning",
                    seconds=str(self.settings.rate_limit_window_seconds),
                )
            )
            return None

        bucket.append(now)
        return await handler(event, data)
