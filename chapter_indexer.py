import json
from typing import Any

from helpers import get_extractions
from models import ChapterIndex

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
        

        
