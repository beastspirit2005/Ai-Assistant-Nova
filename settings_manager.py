import sqlite3
from pathlib import Path


class SettingsManager:
    def __init__(self):
        self.db_path = Path("data/settings.db")
        self.db_path.parent.mkdir(exist_ok=True)

        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_settings(self, settings: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for key, value in settings.items():
            cursor.execute(
                "REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, str(value))
            )

        conn.commit()
        conn.close()

    def load_settings(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT key, value FROM settings")
        rows = cursor.fetchall()

        conn.close()

        settings = {}
        for key, value in rows:
            if value.lower() == "true":
                settings[key] = True
            elif value.lower() == "false":
                settings[key] = False
            else:
                settings[key] = value

        return settings
