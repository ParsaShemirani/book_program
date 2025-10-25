from enum import Enum

from pydantic import BaseModel
from openai.types.responses import ParsedResponse as ParsedResponse

class Side(str, Enum):
    left = "left"
    right = "right"


class FigureType(str, Enum):
    image = "image"
    table = "table"
    plot = "plot"
    other = "other"


class Figure(BaseModel):
    type: FigureType
    name: str | None
    caption: str | None


class Page(BaseModel):
    blank: bool
    starting_section: bool
    side: Side | None
    number: int | None
    header: str | None
    footer: str | None
    figures: list[Figure] = []
    main_text: str | None


class SectionType(str, Enum):
    front_matter = "front_matter"
    chapter = "chapter"
    back_matter = "back_matter"

class Section(BaseModel):
    type: SectionType
    number: int
    name: str
    scan_index: int | None