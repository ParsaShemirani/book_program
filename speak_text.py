import os
from pathlib import Path
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv(key="OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise(ValueError("TIMIDMAN"))


client = OpenAI(api_key=OPENAI_API_KEY)

output_file_path = Path("/Users/parsashemirani/Main/book_program/outputs/speechify.mp3")


with open('/Users/parsashemirani/Main/book_program/outputs/jimmy.md', 'r') as f:
    text = f.read()

instructions = """\
Affect: A gentle, curious narrator with a British accent, guiding a magical, child-friendly adventure through a fairy tale world.

Tone: Magical, warm, and inviting, creating a sense of wonder and excitement for young listeners.

Pacing: Steady and measured, with slight pauses to emphasize magical moments and maintain the storytelling flow.

Emotion: Wonder, curiosity, and a sense of adventure, with a lighthearted and positive vibe throughout.

Pronunciation: Clear and precise, with an emphasis on storytelling, ensuring the words are easy to follow and enchanting to listen to.
"""



with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="shimmer",
    input=text,
    instructions=instructions,
) as response:
    response.stream_to_file(output_file_path)