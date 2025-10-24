import asyncio
from pathlib import Path

from openai import AsyncOpenAI

from extractor import generate_extraction
from env_vars import OPENAI_API_KEY, PAGE_SCAN_DIR, EXTRACTION_RESPONSE_DIR

MAX_CONCURRENCY = 5


client = AsyncOpenAI(api_key=OPENAI_API_KEY)



async def generate_and_save_extraction(file_path: Path):
    response = await generate_extraction(openai_client=client, image_path=file_path)
    output_path = EXTRACTION_RESPONSE_DIR / f"{file_path.stem}.json"
    output_path.write_text(response.model_dump_json(indent=2, by_alias=True))

async def main():
    file_paths = [
        f for f in PAGE_SCAN_DIR.glob("*")
        if not f.name.startswith(".") and f.is_file()
    ]
    file_paths_sorted = sorted(file_paths, key=lambda p: p.name)

    

