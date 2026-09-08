import json
import winsound
from typing import Any

from ollama import ChatResponse, chat

from .stt import STT
from .tts import TTS

TTS.initialize()


class Ripley:
    def __init__(self, system="cli") -> None:
        self._system = system

    def __generate_response(self, msg: str) -> dict:
        response: ChatResponse = chat(
            model="ripley",
            messages=[
                {
                    "role": "user",
                    "content": msg,
                },
            ],
            format="json",
        )

        try:
            ripley_data = json.loads(response.message.content)
            return ripley_data

        except json.JSONDecodeError as e:
            raise RuntimeError("Failed to parse output.") from e

    def speak(self, msg: str):
        response: Any = self.__generate_response(msg)
        TTS.speak(response.get("speech"))

        if self._system == "cli":
            winsound.PlaySound("output.wav", winsound.SND_FILENAME)

        return response.get("speech")


if __name__ == "__main__":
    TTS.initialize()
    stt = STT()
    agent = Ripley()

    running = True
    print("\nRipley is online. Say 'Ripley quit' to exit.")

    while running:
        msg = stt.listen_for_command()

        if not msg:
            continue

        if msg in ["quit", "stop", "exit"]:
            agent.speak("Goodbye, shutting down.")
            running = False
            break

        response = agent.speak(msg)
        print(f"Ripley: {response}")
