"""Async SQLite layer for users, messages, and leads."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import aiosqlite


class Database:
    """Wrap SQLite operations in clear async helper methods."""

    def __init__(self, db_path: str = "bot.sqlite3") -> None:
        """Store the database path and prepare the connection holder."""

        self.db_path = Path(db_path)
        self.connection: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        """Open a database connection and enable useful SQLite settings."""

        self.connection = await aiosqlite.connect(self.db_path)
        self.connection.row_factory = aiosqlite.Row
        await self.connection.execute("PRAGMA foreign_keys = ON;")

    async def close(self) -> None:
        """Close the database connection if it exists."""

        if self.connection is not None:
            await self.connection.close()

    async def init_models(self) -> None:
        """Create all required tables and indexes."""

        connection = self._get_connection()
        await connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT NOT NULL,
                language TEXT NOT NULL DEFAULT 'en',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lead_type TEXT NOT NULL,
                service_code TEXT,
                service_name TEXT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                request TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
            CREATE INDEX IF NOT EXISTS idx_leads_user_id ON leads(user_id);
            CREATE INDEX IF NOT EXISTS idx_leads_type ON leads(lead_type);
            """
        )
        await connection.commit()

    async def upsert_user(
        self,
        user_id: int,
        username: str | None,
        full_name: str,
        language: str,
    ) -> None:
        """Create or update a bot user record."""

        connection = self._get_connection()
        await connection.execute(
            """
            INSERT INTO users (user_id, username, full_name, language)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name,
                language = excluded.language,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, username, full_name, language),
        )
        await connection.commit()

    async def update_user_language(self, user_id: int, language: str) -> None:
        """Update only the stored language of a user."""

        connection = self._get_connection()
        await connection.execute(
            """
            UPDATE users
            SET language = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (language, user_id),
        )
        await connection.commit()

    async def get_user_language(self, user_id: int) -> str | None:
        """Read a user's saved language if available."""

        connection = self._get_connection()
        async with connection.execute(
            "SELECT language FROM users WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
        return row["language"] if row else None

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        """Store a dialog message for later analytics and AI memory."""

        connection = self._get_connection()
        await connection.execute(
            """
            INSERT INTO messages (user_id, role, content)
            VALUES (?, ?, ?)
            """,
            (user_id, role, content),
        )
        await connection.commit()

    async def get_recent_messages(self, user_id: int, limit: int) -> list[dict[str, Any]]:
        """Return the latest messages in chronological order."""

        connection = self._get_connection()
        async with connection.execute(
            """
            SELECT role, content
            FROM (
                SELECT id, role, content
                FROM messages
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
            )
            ORDER BY id ASC
            """,
            (user_id, limit),
        ) as cursor:
            rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def add_lead(
        self,
        user_id: int,
        lead_type: str,
        service_code: str | None,
        service_name: str | None,
        name: str,
        phone: str,
        request: str,
    ) -> None:
        """Save a new lead or order in the database."""

        connection = self._get_connection()
        await connection.execute(
            """
            INSERT INTO leads (user_id, lead_type, service_code, service_name, name, phone, request)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, lead_type, service_code, service_name, name, phone, request),
        )
        await connection.commit()

    async def get_stats(self) -> dict[str, int]:
        """Return simple aggregate statistics for the admin panel."""

        connection = self._get_connection()

        async def scalar(query: str) -> int:
            """Execute a scalar query and return an integer result."""

            async with connection.execute(query) as cursor:
                row = await cursor.fetchone()
            return int(row[0] or 0)

        return {
            "users": await scalar("SELECT COUNT(*) FROM users"),
            "messages": await scalar("SELECT COUNT(*) FROM messages"),
            "leads": await scalar("SELECT COUNT(*) FROM leads"),
            "orders": await scalar("SELECT COUNT(*) FROM leads WHERE lead_type = 'order'"),
            "requests": await scalar("SELECT COUNT(*) FROM leads WHERE lead_type = 'lead'"),
        }

    def _get_connection(self) -> aiosqlite.Connection:
        """Return an active connection or fail fast if setup is missing."""

        if self.connection is None:
            raise RuntimeError("Database connection is not initialized.")
        return self.connection
