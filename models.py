from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from openai.types.responses import ParsedResponse as ParsedResponse


class Side(str, Enum):
    left = "left"
    right = "right"


class Chapter(BaseModel):
    number: int | None
    name: str | None


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
    side: Side | None
    number: int | None
    header: str | None
    footer: str | None
    chapter: Chapter | None
    figures: list[Figure] = []
    main_text: str | None


class Extraction(BaseModel):
    scan_index: int
    file_path: Path
    response: ParsedResponse
    page: Page

