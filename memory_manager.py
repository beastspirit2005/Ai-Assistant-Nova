import sqlite3
import os
from datetime import datetime

DB_PATH = "data/nova.db"


class MemoryManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile_memory (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                created_at TEXT
            )
        """)

        self.conn.commit()

    

    def remember_profile(self, key, value):
        self.cursor.execute("""
            INSERT INTO profile_memory (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        self.conn.commit()

    def recall_profile(self, key):
        self.cursor.execute(
            "SELECT value FROM profile_memory WHERE key = ?",
            (key,)
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    

    def remember_note(self, note):
        self.cursor.execute("""
            INSERT INTO notes (content, created_at)
            VALUES (?, ?)
        """, (note, datetime.now().isoformat()))
        self.conn.commit()

    def list_notes(self):
        self.cursor.execute(
            "SELECT content FROM notes ORDER BY created_at DESC"
        )
        return [row[0] for row in self.cursor.fetchall()]
