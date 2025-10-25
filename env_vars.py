import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv(key="OPENAI_API_KEY")
BOOK_DIR = Path(os.getenv(key="BOOK_DIR"))


PAGE_SCAN_DIR = BOOK_DIR / "page_scans"
COMPRESSED_PAGE_SCAN_DIR = PAGE_SCAN_DIR / "compressed"