from PyQt5.QtCore import QThread, pyqtSignal
import os

from openai import OpenAI

from core.emotion import EmotionDetector
from core.emotion_memory import EmotionMemory


class AIWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, user_text: str):
        super().__init__()
        self.user_text = user_text

        
        self.emotion_detector = EmotionDetector()
        self.emotion_memory = EmotionMemory()

        
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self):
        try:
            emotion = self.emotion_detector.detect(self.user_text)

            self.emotion_memory.record_emotion(
                emotion["mood"],
                emotion["intensity"]
            )

            soften = self.emotion_memory.should_soften_tone()
            keep_short = self.emotion_memory.should_keep_short()

            system_prompt = (
                "You are Nova, a friendly, respectful, and supportive AI assistant. "
                "Be calm, helpful, and natural."
            )

            if soften:
                system_prompt += (
                    " The user seems emotionally strained. "
                    "Respond gently and empathetically. Avoid being playful."
                )

            if keep_short:
                system_prompt += (
                    " Keep responses concise and avoid unnecessary follow-up questions."
                )

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": self.user_text}
                ],
                temperature=0.6
            )

            reply = response.choices[0].message.content.strip()
            self.finished.emit(reply)

        except Exception as e:
            print("AIWorker error:", repr(e))
            self.finished.emit(
                "Sorry, something went wrong while processing your request."
            )
