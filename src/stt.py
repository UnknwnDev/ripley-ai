from RealtimeSTT import AudioToTextRecorder

WAKE_WORDS = ["hey ripley", "ok ripley", "okay ripley", "ripley"]


class STT:
    def __init__(self) -> None:
        self.wake_words = sorted([w.lower() for w in WAKE_WORDS], key=len, reverse=True)

        print("Initializing STT Engine...")
        self.recorder = AudioToTextRecorder(  # type:ignore
            ensure_sentence_ends_with_period = False,
            transcription_engine="whisper_cpp",
            model="tiny.en",
            device="cpu",
            beam_size=1,
            language="en",
            spinner=False
        )

    def stop_listening(self):
        """Temporarily pause audio intake."""
        self.recorder.stop()

    def start_listening(self):
        """Resume audio intake."""
        self.recorder.start()

    def clear_buffer(self):
        """Purges residual speaker audio from the RealtimeSTT queue."""
        self.recorder.flush_audio_input()

    def listen_for_command(self, follow_up: bool = False) -> str:
        self.clear_buffer()

        print(f"\nListening... {'Follow up' if follow_up else ''}")

        text = self.recorder.text()


        text_lower = text.lower().strip()
        text_lower = text_lower.lstrip(" ,.?!'")
        text_lower = text_lower.strip(" ,.?!'").strip()

        # Filter out Whisper silence tokens
        if not text_lower or "[blank_audio]" in text_lower:
            return ""

        if follow_up:
            print(f"User: {text}")
            return text_lower

        ending_phrases = [
            "thank you ripley",
            "thanks ripley",
            "goodbye ripley",
            "bye ripley",
        ]
        for phrase in ending_phrases:
            if text_lower.endswith(phrase) or phrase in text_lower:
                print(f"User: {text}")
                return phrase

        for wake_word in self.wake_words:
            idx = text_lower.find(wake_word)

            if idx != -1 and idx <= 4:
                command = text_lower[idx + len(wake_word) :].strip()
                command = command.lstrip(" ,.?!").strip()
                print(f"User: {text}")
                if not command:
                    command = "Hello"

                return command

        return ""
