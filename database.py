"""Capa de acceso a datos: SQLite local para tareas y notas."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

APP_DIR = Path.home() / ".gestor_personal"
APP_DIR.mkdir(exist_ok=True)
DB_PATH = APP_DIR / "datos.db"


@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    category: str
    priority: str  # Baja, Media, Alta
    due_date: str  # ISO date string o ""
    completed: bool
    created_at: str


@dataclass
class Note:
    id: Optional[int]
    title: str
    content: str
    category: str
    pinned: bool
    created_at: str
    updated_at: str


class Database:
    def __init__(self, path: Path = DB_PATH):
        self.conn = sqlite3.connect(str(path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                category TEXT DEFAULT 'General',
                priority TEXT DEFAULT 'Media',
                due_date TEXT DEFAULT '',
                completed INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT DEFAULT '',
                category TEXT DEFAULT 'General',
                pinned INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            """
        )
        self.conn.commit()

    # ---------- Settings ----------
    def get_setting(self, key: str, default: str = "") -> str:
        row = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default

    def set_setting(self, key: str, value: str) -> None:
        self.conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        self.conn.commit()

    # ---------- Tasks ----------
    def add_task(self, title: str, description: str, category: str, priority: str, due_date: str) -> int:
        cur = self.conn.execute(
            "INSERT INTO tasks (title, description, category, priority, due_date, completed, created_at) "
            "VALUES (?, ?, ?, ?, ?, 0, ?)",
            (title, description, category, priority, due_date, datetime.now().isoformat(timespec="seconds")),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_task(self, task_id: int, **fields) -> None:
        if not fields:
            return
        columns = ", ".join(f"{k}=?" for k in fields)
        values = list(fields.values()) + [task_id]
        self.conn.execute(f"UPDATE tasks SET {columns} WHERE id=?", values)
        self.conn.commit()

    def delete_task(self, task_id: int) -> None:
        self.conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def get_tasks(self) -> list[Task]:
        rows = self.conn.execute("SELECT * FROM tasks ORDER BY completed ASC, due_date IS NULL, due_date ASC, id DESC").fetchall()
        return [
            Task(
                id=r["id"], title=r["title"], description=r["description"], category=r["category"],
                priority=r["priority"], due_date=r["due_date"], completed=bool(r["completed"]),
                created_at=r["created_at"],
            )
            for r in rows
        ]

    def task_categories(self) -> list[str]:
        rows = self.conn.execute("SELECT DISTINCT category FROM tasks ORDER BY category").fetchall()
        return [r["category"] for r in rows]

    # ---------- Notes ----------
    def add_note(self, title: str, content: str, category: str) -> int:
        now = datetime.now().isoformat(timespec="seconds")
        cur = self.conn.execute(
            "INSERT INTO notes (title, content, category, pinned, created_at, updated_at) "
            "VALUES (?, ?, ?, 0, ?, ?)",
            (title, content, category, now, now),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_note(self, note_id: int, **fields) -> None:
        if not fields:
            return
        fields["updated_at"] = datetime.now().isoformat(timespec="seconds")
        columns = ", ".join(f"{k}=?" for k in fields)
        values = list(fields.values()) + [note_id]
        self.conn.execute(f"UPDATE notes SET {columns} WHERE id=?", values)
        self.conn.commit()

    def delete_note(self, note_id: int) -> None:
        self.conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
        self.conn.commit()

    def get_notes(self) -> list[Note]:
        rows = self.conn.execute("SELECT * FROM notes ORDER BY pinned DESC, updated_at DESC").fetchall()
        return [
            Note(
                id=r["id"], title=r["title"], content=r["content"], category=r["category"],
                pinned=bool(r["pinned"]), created_at=r["created_at"], updated_at=r["updated_at"],
            )
            for r in rows
        ]

    def note_categories(self) -> list[str]:
        rows = self.conn.execute("SELECT DISTINCT category FROM notes ORDER BY category").fetchall()
        return [r["category"] for r in rows]

    def close(self) -> None:
        self.conn.close()
