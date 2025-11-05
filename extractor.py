import base64
import asyncio
from pathlib import Path

from openai import AsyncOpenAI
from openai.types.responses import Response

from helpers import get_sorted_files
from env_vars import OPENAI_API_KEY, TEXT_EXTRACTION_PROMPT_PATH

EXTRACTION_PROMPT = TEXT_EXTRACTION_PROMPT_PATH.read_text()

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def generate_extraction_response(scan_path: Path) -> Response:
    base64_image = encode_image(image_path=scan_path)

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

async def generate_and_save_response(scan_path: Path, output_dir_path: Path) -> None:
    response = await generate_extraction_response(scan_path)
    output_file_path = output_dir_path / f"{scan_path.stem}.json"
    output_file_path.write_text(response.model_dump_json(indent=2))

async def generate_responses_dir(scan_dir_path: Path) -> None:
    responses_dir_path = scan_dir_path / "responses"
    responses_dir_path.mkdir()

    scan_paths = get_sorted_files(scan_dir_path)

    async with asyncio.TaskGroup() as tg:
        for sp in scan_paths:
            tg.create_task(
                generate_and_save_response(sp, responses_dir_path)
            )

def generate_main_text(scan_dir_path: Path) -> None:
    response_paths = get_sorted_files(scan_dir_path / "responses")
    responses = [Response.model_validate_json(rp.read_text()) for rp in response_paths]

    main_text_list = [r.output_text for r in responses]
    main_text = " ".join(main_text_list)

    main_text_path = scan_dir_path / "main_text.md"
    main_text_path.write_text(main_text)
    
