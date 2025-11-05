import asyncio
from pathlib import Path

import typer
from typing_extensions import Annotated


from extractor import extract_text, multiple_extract_and_save_text
from narration import split_narrate_save_text
from helpers import calculate_response_cost, get_sorted_files

def main(
    file_or_directory_str: Annotated[str, typer.Argument()],
    extract: Annotated[bool, typer.Option()] = False,
    narrate: Annotated[bool, typer.Option()] = False,
    save_to_file: Annotated[bool, typer.Option()] = True,
):
    file_or_directory_path = Path(file_or_directory_str)
    if file_or_directory_path.is_file():
        file_path = file_or_directory_path
        dir_path = None
    elif file_or_directory_path.is_dir():
        dir_path = file_or_directory_path
        file_path = None
    else:
        print(f"Path not identified as file or directory: {str(file_or_directory_path)}")
        raise typer.Exit()

    if extract:
        if file_path:
            print(f"Extracting text from file: {str(file_path)}")
            extracted_text_response = asyncio.run(extract_text(file_path=file_path))
            if save_to_file:
                output_path = file_path.parent / f"{file_path.stem}.txt"
                output_path.write_text(extracted_text_response.output_text)
                
            else:
                print(f"Extracted Text: \n{extracted_text_response.output_text}")
            try:
                calculation_cost = calculate_response_cost(response=extracted_text_response)
                print(f"Calculation Cost: ${calculation_cost}")
            except KeyError:
                print("Cost could not be calcuated as pricing data not available for model used.")
        elif dir_path:
            file_paths = get_sorted_files(dir_path=dir_path)
            output_dir_path = dir_path.parent / f"{dir_path.name}_extracted"
            output_dir_path.mkdir(exist_ok=True)
            print(f"Extracting text from files:\n")
            for fp in file_paths:
                print(str(fp))
            
            asyncio.run(multiple_extract_and_save_text(file_paths=file_paths, output_dir_path=output_dir_path))
            print("Done!")
    elif narrate:
        if file_path:
            print(f"Narrating file: {str(file_path)}")
            asyncio.run(split_narrate_save_text(file_path=file_path))


if __name__ == "__main__":
    typer.run(main)
