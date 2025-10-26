import base64
import asyncio
from pathlib import Path

from openai import AsyncOpenAI
from openai.types.responses import ParsedResponse

from models import Page
from helpers import digit_sorter
from env_vars import OPENAI_API_KEY, PAGE_EXTRACTION_PROMPT_PATH, RESPONSES_DIR, PAGE_SCANS_DIR, RESULTS_OUTPUT_PATH

MAX_CONCURRENCY = 20

EXTRACTION_PROMPT = PAGE_EXTRACTION_PROMPT_PATH.read_text()

def encode_image(image_path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def write_results(path_tasks: list[tuple[Path, asyncio.Task[bool]]]) -> None:
    results_string = ""
    for p, t in path_tasks:
        result = t.result()
        results_string += f"{p.stem}: {str(result)}\n"
    RESULTS_OUTPUT_PATH.write_text(results_string)


async def generate_extraction(openai_client: AsyncOpenAI, scan_path: str) -> ParsedResponse[Page]:
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
    return response

async def generate_and_save_extraction(
    scan_path: Path, sem: asyncio.Semaphore, openai_client: AsyncOpenAI
) -> bool:
    print(f"Task started for: {scan_path}")
    async with sem:
        try:
            print(f"Response started for: {scan_path}")
            response = await generate_extraction(
                openai_client=openai_client, scan_path=scan_path
            )
            print(f"Writing output for: {scan_path}")
            output_path = RESPONSES_DIR / f"{scan_path.stem}.json"
            output_path.write_text(response.model_dump_json(indent=2, by_alias=True))
            return True
        except Exception:
            return False


async def main():
    scan_paths = [
        f for f in PAGE_SCANS_DIR.glob("*") if not f.name.startswith(".") and f.is_file()
    ]
    sorted_scan_paths= sorted(scan_paths, key=digit_sorter)
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    path_tasks: list[tuple[Path, asyncio.Task[bool]]] = []
    async with asyncio.TaskGroup() as tg:
        for sp in sorted_scan_paths:
            t = tg.create_task(
                generate_and_save_extraction(
                    scan_path=sp,
                    sem=sem,
                    openai_client=openai_client
                )
            )
            path_tasks.append((sp, t))

    write_results(path_tasks=path_tasks)

if __name__ == "__main__":
    asyncio.run(main())