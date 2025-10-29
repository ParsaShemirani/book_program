import base64
import asyncio
from pathlib import Path

from openai import AsyncOpenAI
from openai.types.responses import ParsedResponse

from models import Page
from helpers import digit_sorter
from env_vars import OPENAI_API_KEY, PAGE_EXTRACTION_PROMPT_PATH

MAX_CONCURRENCY = 20

EXTRACTION_PROMPT = PAGE_EXTRACTION_PROMPT_PATH.read_text()


def encode_image(image_path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def extract_page(
    scan_path: str, openai_client: AsyncOpenAI
) -> ParsedResponse[Page]:
    base64_image = encode_image(image_path=scan_path)

    response = await openai_client.responses.parse(
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
        text_format=Page,
    )
    return response.output_parsed


async def extract_and_save_page(
    scan_path: Path,
    output_path: Path,
    sem: asyncio.Semaphore,
    openai_client: AsyncOpenAI,
) -> bool:
    async with sem:
        try:
            page = await extract_page(scan_path=scan_path, openai_client=openai_client)
            output_path.write_text(page.model_dump_json(indent=2))
            return True
        except Exception as e:
            print(f"FAILURE: {scan_path} | Exception: {e}")


async def main(scan_dir: Path, output_dir: Path):
    scan_paths = [
        f for f in scan_dir.glob("*") if not f.name.startswith(".") and f.is_file()
    ]
    sorted_scan_paths = sorted(scan_paths, key=digit_sorter)

    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async with asyncio.TaskGroup() as tg:
        for s in sorted_scan_paths:
            t = tg.create_task(
                extract_and_save_page(
                    scan_path=s,
                    output_path=(output_dir / s.stem + ".json"),
                    sem=sem,
                    openai_client=openai_client,
                )
            )


if __name__ == "__main__":
    scan_dir = Path(input("Enter scan_dir: "))
    output_dir = Path(input("Enter output_dir: "))

    asyncio.run(main(scan_dir=scan_dir, output_dir=output_dir))
