from pathlib import Path
from openai import OpenAI

from secret_things import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

speech_file_path = Path("/Users/parsashemirani/Main/Inbox/book_programs/outputs/speechify.mp3")


with open('/Users/parsashemirani/Main/Inbox/book_programs/outputs/reconsil.md', 'r') as f:
    text = f.read()

instructions = """\
Speak in a cheerful and positive tone.
"""



with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input=text,
    instructions=instructions,
) as response:
    response.stream_to_file(speech_file_path)