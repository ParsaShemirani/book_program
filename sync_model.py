import base64

from openai import OpenAI
from pydantic import BaseModel

from secret_things import OPENAI_API_KEY



def encode_image(image_path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


client = OpenAI(api_key=OPENAI_API_KEY)

class Chapter(BaseModel):
    number: int | None
    name: str | None

class Figure(BaseModel):
    name: str | None
    caption: str | None

class PageExtraction(BaseModel):
    blank: bool
    observed_number: int | None
    header: str | None
    footer: str | None
    chapter: Chapter | None
    figures: list[Figure] = []
    main_text: str | None



system_prompt = """\
You are an expert in taking an image of a page of a book
and extracting the content of it. Below are the various fields you may
record and how to record them.

blank: If the page is blank, mark true, otherwise mark false.

observed_number: If there is a page number specified in the image, complete the 'observed_number' field with it.
Leave it null if there is no page number. If a roman numeral page number is observed, mark it as null.

header: If a header is observed, extract the plain text representation of it in this field, no line breaks.
Do not include the page number here.

footer: If a footer is observed, extract the plain text representation of it in this field, no line breaks.
Do not include the page number here.

chapter: If the start of a new chapter is specified on this page, extract the chapter number as an integer, and chapter name
as plain text without line breaks if specified.

figures: If any figures are present on the page, extract the name and caption if specified as markdown text, no line breaks.
The name and caption should be exactly as is and left null if not present.


main_text: If there is main text, extract the markdown representation of it in this field.
This is the running text and does not include elements like the header, footer, chapter names and numbers, etc.
It does not include any non text elements either like figures, images, or mathematical notation.
It is what a narrator would read out loud, and does not include diagrams, callouts. Sections of text that are visually
isolated from the flow of the main text should be treated as figures rather than part of the main text.


Do not add, take away, or modify any content. 
Do not complete cut-off sentences. Only extract exactly what is visible.
Extract the content exactly as is and in its full.

Markdown formatting rules you must follow:
- Use `#`, `##`, `###` for section headings if they are visually distinguishable as titles, subtitles, or numbered sections.
- Convert all bulleted lists into proper Markdown lists using `- ` or `* ` instead of OCR bullet characters like `•`.
- Preserve all paragraphs as plain text (separated by a blank line).
- If there are quotations or dialogue, wrap them in Markdown blockquotes using `>`.
- If text is emphasized (italics, bold, underlined in the book), convert it into Markdown emphasis (`*italic*`, `**bold**`).

"""


def generate_extraction(image_path: str):
   base64_image = encode_image(image_path=image_path)


   response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": system_prompt},
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
