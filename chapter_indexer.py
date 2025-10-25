import json
from typing import Any

from helpers import get_extractions
from models import ChapterIndex
from env_vars import BOOK_DIR

extractions = get_extractions()

chapter_index_list: list[dict[str, Any]] = []
for e in extractions:
    if e.page.chapter is not None:
        chapter_index_list.append(
            ChapterIndex(
                scan_index=e.scan_index,
                chapter=e.page.chapter
            ).model_dump()
        )
json_str = json.dumps(chapter_index_list, indent=2)
        
output_path = BOOK_DIR / "chapter_index.json"
output_path.write_text(json_str)