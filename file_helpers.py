from PIL import Image

from env_vars import PAGE_SCAN_DIR


def enumerate_files():
    file_paths = [
        f for f in PAGE_SCAN_DIR.glob("*")
        if not f.name.startswith(".") and f.is_file()
    ]
    file_paths_sorted = sorted(file_paths, key=lambda p: p.name)

    scan_index = 1
    for f in file_paths_sorted:
        target_name = f.parent / f"{scan_index}{f.suffix}"
        f.rename(target=target_name)
        scan_index += 1

def rotate_images(degrees: float):
    file_paths = [
        f for f in PAGE_SCAN_DIR.glob("*")
        if not f.name.startswith(".") and f.is_file()
    ]
    file_paths_sorted = sorted(file_paths, key=lambda p: p.name)

    for f in file_paths_sorted:
        image = Image.open(f)
        image_rotated = image.rotate(angle=degrees, expand=True)
        image_rotated.save(f)
