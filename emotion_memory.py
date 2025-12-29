import sqlite3
from datetime import datetime, timedelta
from collections import Counter
import os


DB_PATH = "data/emotion.db"
MAX_EVENTS_PER_DAY = 20
WINDOW_HOURS = 48


class EmotionMemory:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_table()


    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emotion_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood TEXT NOT NULL,
                intensity REAL NOT NULL,
                time_block TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        self.conn.commit()


    def record_emotion(self, mood: str, intensity: float):
        """
        Records an emotion event in a safe, bounded way.
        """
        intensity = max(0.0, min(1.0, intensity))
        now = datetime.now()

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM emotion_events
            WHERE DATE(timestamp) = DATE(?)
        """, (now.isoformat(),))

        count_today = cursor.fetchone()[0]
        if count_today >= MAX_EVENTS_PER_DAY:
            return  

        time_block = self._get_time_block(now)

        cursor.execute("""
            INSERT INTO emotion_events (mood, intensity, time_block, timestamp)
            VALUES (?, ?, ?, ?)
        """, (mood, intensity, time_block, now.isoformat()))

        self.conn.commit()

    def get_recent_summary(self) -> dict:
        """
        Returns a safe summary of recent emotional state.
        """
        events = self._get_recent_events()
        if not events:
            return {
                "dominant_mood": "neutral",
                "average_intensity": 0.0,
                "trend": "stable",
                "confidence": 0.0
            }

        moods = [e["mood"] for e in events]
        intensities = [e["intensity"] for e in events]

        dominant_mood = Counter(moods).most_common(1)[0][0]
        avg_intensity = round(sum(intensities) / len(intensities), 2)

        trend = self._calculate_trend(intensities)

        confidence = min(1.0, len(events) / 10)

        return {
            "dominant_mood": dominant_mood,
            "average_intensity": avg_intensity,
            "trend": trend,
            "confidence": confidence
        }

    def get_time_pattern(self) -> dict:
        """
        Returns dominant mood by time block.
        """
        events = self._get_recent_events()
        if not events:
            return {}

        pattern = {}
        blocks = ["morning", "afternoon", "evening", "night"]

        for block in blocks:
            block_events = [e["mood"] for e in events if e["time_block"] == block]
            if block_events:
                pattern[block] = Counter(block_events).most_common(1)[0][0]

        return pattern


    def should_soften_tone(self) -> bool:
        summary = self.get_recent_summary()
        return (
            summary["dominant_mood"] in {"stressed", "sad", "angry"} and
            summary["average_intensity"] >= 0.6 and
            summary["confidence"] >= 0.5
        )

    def should_keep_short(self) -> bool:
        summary = self.get_recent_summary()
        return (
            summary["dominant_mood"] in {"tired", "stressed"} and
            summary["average_intensity"] >= 0.5
        )


    def _get_recent_events(self):
        """
        Fetch events within rolling time window.
        """
        since = datetime.now() - timedelta(hours=WINDOW_HOURS)

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT mood, intensity, time_block, timestamp
            FROM emotion_events
            WHERE timestamp >= ?
        """, (since.isoformat(),))

        rows = cursor.fetchall()

        return [
            {
                "mood": r[0],
                "intensity": r[1],
                "time_block": r[2],
                "timestamp": r[3]
            }
            for r in rows
        ]

    def _calculate_trend(self, intensities):
        if len(intensities) < 3:
            return "stable"

        first_half = intensities[:len(intensities)//2]
        second_half = intensities[len(intensities)//2:]

        if sum(second_half) > sum(first_half) + 0.2:
            return "worsening"
        elif sum(first_half) > sum(second_half) + 0.2:
            return "improving"
        return "stable"

    def _get_time_block(self, dt: datetime) -> str:
        hour = dt.hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        return "night"
