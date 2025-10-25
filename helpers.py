import re
from pathlib import Path

from PIL import Image


def digit_sorter(p: Path):
    stem = p.stem
    digits = re.findall(r"\d+", stem)
    if digits:
        print(int(digits[-1]))
        return int(digits[-1])
    else:
        raise (
            ValueError(
                f"Filename does not contain digits to index by. Filename: {str(p)}"
            )
        )


def index_scans(dir: Path, starting_index: int):
    file_paths = [
        f for f in dir.glob("*") if not f.name.startswith(".") and f.is_file()
    ]
    sorted_file_paths = sorted(file_paths, key=digit_sorter)

    scan_index = starting_index
    for f in sorted_file_paths:
        indexed_name = f.parent / f"{scan_index}{f.suffix.lower()}"
        f.rename(indexed_name)
        scan_index += 1

def rotate_images(dir: Path, degrees: float):
    file_paths = [
        f for f in dir.glob("*")
        if not f.name.startswith(".") and f.is_file()
    ]

    for f in file_paths:
        image = Image.open(f)
        image_rotated = image.rotate(angle=degrees, expand = True)
        image_rotated.save(f)