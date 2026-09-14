import base64

from fastapi import FastAPI
from pydantic import BaseModel

from src.agent import Ripley

app = FastAPI()
agent = Ripley()


class CommandRequest(BaseModel):
    query: str


@app.put('/api/v1/commands')
def execute_command(request: CommandRequest):
    query = request.query
    intent, speech = agent.speak(query)
    with open("output.wav", 'rb') as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')

    return {
           "intent": intent,
           "speech": speech,
           "audio": {"format": "wav", "base64": encoded_audio}
       }

# if __name__ == "__main__":
app.frontend('/', directory='frontend', fallback='index.html')
