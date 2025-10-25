from helpers import get_extractions
from env_vars import CHAPTER_DIR



def create_chapter_folder(chapter_number: int, start_scan_index: int, end_scan_index: int):
    scan_index_range = range(start_scan_index, end_scan_index + 1)

    chapter_responses_folder = CHAPTER_DIR / str(chapter_number) / "responses"
    chapter_responses_folder.mkdir(parents=True)

    extractions = get_extractions()

    for e in extractions:
        if e.scan_index in scan_index_range:
            output_path = chapter_responses_folder / f"{e.scan_index}.json"
            output_path.write_text(e.response.model_dump_json(indent=2, by_alias=True))


