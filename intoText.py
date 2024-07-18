from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openAIkey = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openAIkey)

audio_file = open("outputs/test.mp3", "rb")
transcript = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="text"
)

with open("outputs/transcript.txt", "w", encoding="utf-8") as text_file:
    text_file.write(transcript)