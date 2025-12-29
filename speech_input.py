import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class SpeechInput:
    def __init__(self, model_path="voice/models/vosk-model-small-en-us-0.15"):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio_queue = queue.Queue()
        self.stream = None
        self.text = ""

    def _callback(self, indata, frames, time, status):
        self.audio_queue.put(bytes(indata))

    def start_listening(self):
        self.text = ""
        self.stream = sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._callback
        )
        self.stream.start()

    def stop_and_transcribe(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()

        while not self.audio_queue.empty():
            data = self.audio_queue.get()
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                self.text += result.get("text", "") + " "

        return self.text.strip()
