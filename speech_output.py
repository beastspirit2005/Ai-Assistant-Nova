import pyttsx3
import threading


class SpeechOutput:
    def speak(self, text: str):
        if not text:
            print("SpeechOutput: empty text")
            return

        threading.Thread(
            target=self._speak_blocking,
            args=(text,),
            daemon=True
        ).start()

    def _speak_blocking(self, text: str):
        try:
            engine = pyttsx3.init(driverName="sapi5")
            engine.setProperty("rate", 175)
            engine.setProperty("volume", 1.0)

            print("Speaking:", text)  
            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("Speech error:", e)
