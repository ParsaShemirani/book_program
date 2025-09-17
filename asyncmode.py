import base64
import asyncio

from openai import AsyncOpenAI
from pydantic import BaseModel

from secret_things import OPENAI_API_KEY



def encode_image(image_path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


client = AsyncOpenAI(api_key=OPENAI_API_KEY)


class PageExtraction(BaseModel):
    blank: bool
    number: int | None
    markdown_content: str | None


system_prompt = """\
You are an expert in taking an image of a page of a book
and extracting the content of it. First, you should check if it is a blank page or not.
If it is blank, you shall mark blank as true and leave the other two fields null.
If there is a page number specified, you should complete the 'number' field for the response specifying
it, leave it null if there is no page number. Do not include a roman numeral page number, instead mark as null.
Also do not include any heading or footers or page number as part of the markdown content.

If there is content, you will generate the **Markdown extraction** of the content of the page.
Markdown formatting rules you must follow:
- Use `#`, `##`, `###` for section headings if they are visually distinguishable as titles, subtitles, or numbered sections.
- Convert all bulleted lists into proper Markdown lists using `- ` or `* ` instead of OCR bullet characters like `•`.
- Preserve all paragraphs as plain text (separated by a blank line).
- If there are quotations or dialogue, wrap them in Markdown blockquotes using `>`.
- If text is emphasized (italics, bold, underlined in the book), convert it into Markdown emphasis (`*italic*`, `**bold**`).
- For non-text elements such as images, figures, charts, or diagrams, write them in Markdown image syntax without a link or file path. Provide a short description or caption as the alt text inside square brackets.
  Example:
  `![Figure 1: This chart shows the growth of the population throughout the twenty-first century]`


Do not add, take away, or modify any content. 
Do not complete cut-off sentences. Only extract exactly what is visible.
"""



async def generate_extraction(image_path: str) -> PageExtraction:
   base64_image = encode_image(image_path=image_path)


   response = await client.responses.parse(
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
   return response.output_parsed






with open ("/Users/parsashemirani/main/inbox/book_programs/outputs/reconsil.md", "w") as f:
    f.write(response.output_parsed.markdown_content)

jimmy = client.responses.retrieve()