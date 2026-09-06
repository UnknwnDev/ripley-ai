import json
import winsound
from typing import Any

from ollama import ChatResponse, chat

from .tts import TTS

TTS.initialize()


class Ripley:
    def __init__(self, system='cli') -> None:
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
            # print("Intent:", ripley_data.get("intent"))
            # print("Speech:", ripley_data.get("speech"))
            return ripley_data

        except json.JSONDecodeError as e:
            raise RuntimeError("Failed to parse output.") from e

    def speak(self, msg: str):
        response: Any = self.__generate_response(msg)
        TTS.speak(response.get("speech"))
        # print("Playing sound")
        if self._system == "cli":
            winsound.PlaySound("output.wav", winsound.SND_FILENAME)

        return response.get("speech")


if __name__ == '__main__':
    agent = Ripley()

    running = True
    print("Enter input here: /q to quit")
    while running:
        msg = input(">> ")
        if msg == "/q":
            agent.speak("Goodbye, Ripley")
            running = False
            break

        response = agent.speak(msg)
        print(f"Ripley: {response}")
