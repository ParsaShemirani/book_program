import json

from env_vars import BOOK_DIR
from models import Section, SectionType

SECTIONS_FILE = BOOK_DIR / "sections.json"


def add_section(section):
    json_str = SECTIONS_FILE.read_text()
    try:
        section_list = [Section.model_validate(s) for s in json.loads(json_str)]
    except json.decoder.JSONDecodeError:
        section_list = []

    section_list.append(section)

    dict_list = [s.model_dump() for s in section_list]
    json_str = json.dumps(dict_list, indent=2)
    SECTIONS_FILE.write_text(json_str)


def interactive_add_session():
    str_input_type = input("Section Type: ")
    try:
        input_type = SectionType(str_input_type)
    except ValueError:
        raise ValueError(f"Section type can only be 'front_matter', 'chapter', or 'back_matter'. Your input: {str_input_type}")

    input_number = int(input("Section Number: "))
    input_name = input("Section Name: ")

    section = Section(type=input_type, number=input_number, name=input_name)
    add_section(section=section)

if __name__ == "__main__":
    interactive_add_session()