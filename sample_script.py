import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv(key="OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise(ValueError("TIMIDMAN"))
client = OpenAI(api_key=OPENAI_API_KEY)

