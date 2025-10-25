import json

from models import Section, SectionType

from env_vars import SECTIONS_PATH


def add_section(section):
    sections_str = SECTIONS_PATH.read_text()
    try:
        section_list = [Section.model_validate(s) for s in json.loads(sections_str)]
    except json.decoder.JSONDecodeError:
        section_list = []

    section_list.append(section)

    dict_list = [s.model_dump() for s in section_list]
    updated_sections_str = json.dumps(dict_list, indent=2)
    SECTIONS_PATH.write_text(updated_sections_str)


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