import base64

from openai import AsyncOpenAI
from openai.types.responses.parsed_response import ParsedResponse

from models import Page

with open("page_extraction_prompt.md", "r") as f:
    PAGE_EXTRACTION_PROMPT = f.read()


def encode_image(image_path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def generate_extraction(openai_client: AsyncOpenAI, image_path: str) -> ParsedResponse[Page]:
    base64_image = encode_image(image_path=image_path)

    response = await openai_client.responses.parse(
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
        text_format=Page,
    )
    return response


def retrieve_page_extraction(response_json: str) -> Page:
    json_text = response_json["output"][1]["content"][0]["text"]
    page_extraction = Page.model_validate_json(json_text)
    return page_extraction

