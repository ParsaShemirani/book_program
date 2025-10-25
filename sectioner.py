import json

from models import Section

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
    input_number = int(input("Section Number: "))
    input_name = input("Section Name: ")

    

if __name__ == "__main__":
    interactive_add_session()