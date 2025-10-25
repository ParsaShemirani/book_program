import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv(key="OPENAI_API_KEY")
PAGE_SCAN_DIR = Path(os.getenv(key="PAGE_SCAN_DIR"))
RESPONSE_DIR = Path(os.getenv(key="RESPONSE_DIR"))

