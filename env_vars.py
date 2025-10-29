import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv(key="OPENAI_API_KEY")

PAGE_EXTRACTION_PROMPT_PATH = Path(__file__).parent / "page_extraction_prompt.md"