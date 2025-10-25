from env_vars import CHAPTER_DIR

chapter_number = 3
MAX_SECTION_LENGTH = 2000

(CHAPTER_DIR / str(chapter_number) / "text_splits").mkdir()

main_text_path = CHAPTER_DIR / str(chapter_number) / "main_text.md"

main_text = main_text_path.read_text()

lines = main_text.split("\n\n")

new_split = ""
split_counter = 1
for l in lines:
    potential_split = new_split + "\n\n" + l
    if len(potential_split) < MAX_SECTION_LENGTH:
        new_split = potential_split
    else:
        output_path = CHAPTER_DIR / str(chapter_number) / "text_splits" /f"{split_counter}.md"
        output_path.write_text(new_split)
        new_split = l
        split_counter += 1