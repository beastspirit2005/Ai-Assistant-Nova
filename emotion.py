import re
from typing import Dict


class EmotionDetector:
    """
    Rule-based emotion detector.
    Detects user's emotional tone from text input.
    """

    def __init__(self):
        
        self.emotion_keywords = {
            "happy": [
                "happy", "excited", "glad", "great", "awesome", "amazing",
                "good day", "feeling good", "nice", "love"
            ],
            "calm": [
                "calm", "relaxed", "peaceful", "okay", "fine", "normal"
            ],
            "tired": [
                "tired", "exhausted", "sleepy", "drained", "burnt out"
            ],
            "stressed": [
                "stressed", "stress", "pressure", "overwhelmed", "tense",
                "too much", "busy", "deadline"
            ],
            "sad": [
                "sad", "down", "upset", "low", "unhappy", "lonely", "hurt"
            ],
            "angry": [
                "angry", "mad", "annoyed", "frustrated", "irritated", "pissed"
            ]
        }

        
        self.intensity_boosters = [
            "very", "really", "so", "extremely", "too", "super"
        ]


    def detect(self, text: str) -> Dict[str, float]:
        """
        Returns:
        {
            "mood": str,
            "intensity": float (0.0 - 1.0)
        }
        """
        if not text or len(text.strip()) < 3:
            return {
                "mood": "neutral",
                "intensity": 0.0
            }

        text_lower = text.lower()

        detected_mood = "neutral"
        base_intensity = 0.3

        
        for mood, keywords in self.emotion_keywords.items():
            for kw in keywords:
                if re.search(r"\b" + re.escape(kw) + r"\b", text_lower):
                    detected_mood = mood
                    base_intensity = 0.6
                    break
            if detected_mood != "neutral":
                break

        
        for booster in self.intensity_boosters:
            if re.search(r"\b" + booster + r"\b", text_lower):
                base_intensity += 0.15

        
        intensity = max(0.0, min(1.0, round(base_intensity, 2)))

        return {
            "mood": detected_mood,
            "intensity": intensity
        }
