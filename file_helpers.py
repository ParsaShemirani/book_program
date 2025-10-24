from pathlib import Path

directory_path = Path("/Users/parsahome/inbox/book_test_inputs/")

files = list(directory_path.glob("*"))
files_sorted: list[Path] = sorted(files, key=lambda p: p.name)

scan_index = 0
for f in files_sorted:
    target_name = f.parent / f"{scan_index}{f.suffix}"
    f.rename(target=target_name)
    scan_index += 1