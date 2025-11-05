import base64
import asyncio
from pathlib import Path

from openai import AsyncOpenAI
from openai.types.responses import Response

from helpers import get_sorted_files
from env_vars import OPENAI_API_KEY, TEXT_EXTRACTION_PROMPT_PATH

MAX_CONCURRENCY = 20

EXTRACTION_PROMPT = TEXT_EXTRACTION_PROMPT_PATH.read_text()

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def extract_text(file_path: Path) -> Response:
    base64_image = encode_image(image_path=file_path)

    response = await openai_client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": EXTRACTION_PROMPT},
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    }
                ],
            },
        ],
    )
    return response


async def extract_and_save_text(
    file_path: Path, output_path: Path, sem: asyncio.Semaphore | None = None
) -> bool:
    if not sem:
        sem = asyncio.Semaphore(1)

    async with sem:
        try:
            response = await extract_text(file_path=file_path)
        except Exception as e:
            print(
                f"FAILIURE generating response for file path {file_path}.\nException: {e}"
            )
            return False

        try:
            output_path.write_text(response.output_text)
        except Exception as e:
            print(f"FAILIURE writing text for file path {file_path}.\nException: {e}")
            return False


async def multiple_extract_and_save_text(
    file_paths: list[Path], output_dir_path: Path
) -> None:
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    async with asyncio.TaskGroup() as tg:
        for fp in file_paths:
            tg.create_task(
                extract_and_save_text(
                    file_path=fp,
                    output_path=output_dir_path / f"{fp.stem}.txt",
                    sem=sem,
                )
            )


"""
async def extract_dir_text(scan_dir: Path, output_dir: Path):
    sorted_scan_paths = get_sorted_files(scan_dir)

    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    async with asyncio.TaskGroup() as tg:
        for s in sorted_scan_paths:
            tg.create_task(
                extract_and_save_text(
                    scan_path=s, output_path=(output_dir / f"{s.stem}.md"), sem=sem
                )
            )
            
"""
