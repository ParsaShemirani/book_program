import asyncio
from pathlib import Path

from openai import AsyncOpenAI

from extractor import generate_extraction
from env_vars import OPENAI_API_KEY, PAGE_SCAN_DIR, RESPONSE_DIR

MAX_CONCURRENCY = 20


async def generate_and_save_extraction(
    file_path: Path, sem: asyncio.Semaphore, openai_client: AsyncOpenAI
) -> bool:
    print(f"TASK BEF SEM STARTED: {file_path}")
    async with sem:
        try:
            print(f"SEMAPHORE PASSED, NOW STARTING RESPONSE for {file_path}")
            response = await generate_extraction(
                openai_client=openai_client, image_path=file_path
            )
            print(f"RESPONSE GENERATED, NOW WRITING OUTPUT FOR {file_path}")
            output_path = RESPONSE_DIR / f"{file_path.stem}.json"
            output_path.write_text(response.model_dump_json(indent=2, by_alias=True))
            return True
        except Exception as e:
            return False


async def main():
    file_paths = [
        f for f in PAGE_SCAN_DIR.glob("*") if not f.name.startswith(".") and f.is_file()
    ]
    file_paths_sorted = sorted(file_paths, key=lambda p: int(p.stem))

    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    tasks: list[tuple[Path, asyncio.Task[bool]]] = []
    async with asyncio.TaskGroup() as tg:
        for file_path in file_paths_sorted:
            t = tg.create_task(
                generate_and_save_extraction(
                    file_path=file_path, sem=sem, openai_client=openai_client
                )
            )
            tasks.append((file_path, t))
            

    results_string = ""
    for file_path, task in tasks:
        result = task.result()
        results_string += f"{file_path.stem}: {str(result)}\n"

    results_output_path = BOOK_DIR / "results.txt"
    results_output_path.write_text(results_string)
    print("Wrote results")

    


asyncio.run(main())
