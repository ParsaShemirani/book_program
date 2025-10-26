import json
from pathlib import Path

from openai.types.responses import ParsedResponse

from models import Section, Page
from env_vars import SECTIONS_PATH, RESPONSES_DIR


def add_section(section):
    try:
        section_list = [Section.model_validate(s) for s in json.loads(SECTIONS_PATH.read_text())]
    except json.decoder.JSONDecodeError:
        section_list = []

    section_list.append(section)

    dict_list = [s.model_dump() for s in section_list]
    updated_sections_str = json.dumps(dict_list, indent=2)
    SECTIONS_PATH.write_text(updated_sections_str)


def interactive_add_session():
    add_section(
        Section(
            number=int(input("Section Number: ")),
            name=input("Section Name: "),
            starting_scan_index=int(input("Starting Scan Index: ")),
            ending_scan_index=input("Ending Scan Iddex: ")
        )
    )






if __name__ == "__main__":
    interactive_add_session()