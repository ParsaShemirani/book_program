from env_vars import CHAPTER_DIR
from helpers import get_extractions

chapter_number = 3

chapter_responses_dir = CHAPTER_DIR / str(chapter_number) / "responses"

extractions = get_extractions(directory=chapter_responses_dir)

chapter_markdown = ""

for e in extractions:
    chapter_markdown += e.page.main_text + 2*"\n"

output_path_markdown = CHAPTER_DIR / str(chapter_number) / "main_text.md"

output_path_markdown.write_text(chapter_markdown)