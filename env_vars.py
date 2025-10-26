import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv(key="OPENAI_API_KEY")

PAGE_EXTRACTION_PROMPT_PATH = Path(__file__).parent / "page_extraction_prompt.md"

BOOK_DIR = Path(os.getenv(key="BOOK_DIR"))
SECTIONS_PATH = BOOK_DIR / "sections.json"
RESULTS_OUTPUT_PATH = BOOK_DIR / "results.txt"
PAGE_SCANS_DIR = BOOK_DIR / "page_scans"
RESPONSES_DIR = BOOK_DIR / "responses"
TEMP_DIR = BOOK_DIR / "temp"