from enum import Enum

from pydantic import BaseModel

class Side(str, Enum):
    left = "left"
    right = "right"

class Page(BaseModel):
    blank: bool
    number: int | None
    main_text: str | None


class Section(BaseModel):
    number: int
    name: str
    starting_scan_index: int
    ending_scan_index: int