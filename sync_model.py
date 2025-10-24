import base64
import os
from enum import Enum

from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise (ValueError("TIMIDMAN"))

with open("page_extraction_prompt.md", "r") as f:
    PAGE_EXTRACTION_PROMPT = f.read()


def encode_image(image_path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class Chapter(BaseModel):
    number: int | None
    name: str | None


class FigureType(str, Enum):
    image = "image"
    table = "table"
    plot = "plot"
    text = "text"
    other = "other"


class Figure(BaseModel):
    type: FigureType
    name: str | None
    caption: str | None


class PageExtraction(BaseModel):
    blank: bool
    page_number: int | None
    header: str | None
    footer: str | None
    chapter: Chapter | None
    figures: list[Figure] = []
    main_text: str | None


def generate_extraction(openai_client: OpenAI, image_path: str):
    base64_image = encode_image(image_path=image_path)

    response = openai_client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": PAGE_EXTRACTION_PROMPT},
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
        text_format=PageExtraction,
    )
    return response


"""
import json
response_json = response.model_dump_json(indent = 2)
parsed = response.output_parsed
main_text = parsed.main_text
"""


"""
with open("/Users/parsashemirani/Main/book_program/outputs/reminate11.md", "w") as f:
    f.write(main_text)
"""


"""
with open("/Users/parsashemirani/Main/book_program/outputs/timdust2.json", "w") as f:
    f.write(response_json)
"""


def retrieve_parsed(response_json: dict):
    for output in response_json.get("output", []):
        contents = output.get("content") or []
        for content in contents:
            if isinstance(content, dict) and "parsed" in content:
                return content["parsed"]
    return None
