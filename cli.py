import asyncio
from pathlib import Path
from typing_extensions import Annotated

import typer

from helpers import get_sorted_files
from extractor import generate_responses_dir, generate_main_text

def main(
    scan_dir: Annotated[str, typer.Argument()]
):
    scan_dir_path = Path(scan_dir)
    if not scan_dir_path.is_dir():
        print(f"Path not identified as directory: {str(scan_dir_path)}")
        raise typer.Exit()

    print("Generating Responses")
    asyncio.run(generate_responses_dir(scan_dir_path))

    print("Generating Main Text")
    generate_main_text(scan_dir_path)

    print("Generating Text Splits")


if __name__ == "__main__":
    typer.run(main)
