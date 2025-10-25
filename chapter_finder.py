from pathlib import Path
from openai.types.responses.parsed_response import ParsedResponse

from extractor import Page, Chapter
from env_vars import RESPONSE_DIR

def is_integer_stem(file_path: Path) -> bool:
    try:
        int(file_path.stem)
        return True
    except ValueError:
        return False
    

file_paths = [
    f
    for f in RESPONSE_DIR.glob("*")
    if not f.name.startswith(".") and f.is_file() and is_integer_stem(f)
]
file_paths_sorted = sorted(file_paths, key=lambda p: int(p.stem))

responses: list[tuple[Path, ParsedResponse[Page]]] = []
for f in file_paths_sorted:
    response_string = f.read_text()
    r = ParsedResponse.model_validate_json(json_data=response_string)
    responses.append((f, r))

chapter_pages: list[tuple[Path, Chapter]] = []

for f, r in responses:
    page_extraction = Page.model_validate(r.output_parsed)
    chapter = page_extraction.chapter
    if chapter is not None:
        chapter_pages.append((f, chapter))