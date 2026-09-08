from RealtimeSTT import AudioToTextRecorder

WAKE_WORDS = ["hey ripley", "ok ripley", "okay ripley", "ripley"]

class STT:
    def __init__(self) -> None:
        self.wake_words = sorted([w.lower() for w in WAKE_WORDS], key=len, reverse=True)

        print("Initializing STT Engine...")
        self.recorder = AudioToTextRecorder( # type:ignore
            transcription_engine="whisper_cpp",
            model="tiny.en",
            device="cpu",
            language="en",
            post_speech_silence_duration=0.25,
            silero_deactivity_detection=True,
            silero_use_onnx=False,
            transcription_engine_options={
                "model": {"n_threads": 4},
                "transcribe": {"single_segment": True, "no_context": True},
            },
        )

    def pause(self):
        self.recorder.stop()

    def resume(self):
        self.recorder.start()

    def listen_for_command(self) -> str:
            print(f"\nListening...")

            while True:
                text = self.recorder.text()
                text_lower = text.lower().strip()
                text_lower = text_lower.lstrip(" ,.?!'")

                ending_phrases = ["thank you ripley", "thanks ripley", "goodbye ripley", "bye ripley"]
                for phrase in ending_phrases:
                    if text_lower.endswith(phrase) or phrase in text_lower:
                        # print(f"User: {text}")
                        return phrase

                for wake_word in self.wake_words:
                    idx = text_lower.find(wake_word)

                    if idx != -1 and idx <= 4:
                        print(f"User: {text}")

                        command = text_lower[idx + len(wake_word):].strip()
                        command = command.lstrip(" ,.?!").strip()

                        if not command:
                            command = "Hello"

                        return command
