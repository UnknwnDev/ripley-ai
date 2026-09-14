import json
import time
from typing import Any

from dotenv import find_dotenv, load_dotenv
from ollama import ChatResponse, chat

from .stt import STT
from .tts import TTS

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class Ripley:
    def __init__(self) -> None:
        TTS.initialize()

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
        speech_text = response.get("speech", "")

        TTS.speak(speech_text)

        return response.get("intent"), speech_text


    # TTS.initialize()
    # stt = STT()
    # agent = Ripley(stt=stt)

    # running = True
    # print("\nRipley is online. Say 'Ripley quit' to exit.")

    # while running:
    #     msg = stt.listen_for_command()

    #     if not msg:
    #         continue

    #     if msg.lower() in ["quit", "stop", "exit"]:
    #         agent.speak("Goodbye, shutting down.")
    #         stt.recorder.shutdown()
    #         running = False
    #         break

    #     agent.stt.stop_listening()
    #     intent, speech = agent.speak(msg)
    #     print(f"Ripley: {speech}")
