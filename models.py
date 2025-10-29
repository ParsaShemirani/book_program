from pydantic import BaseModel

class Page(BaseModel):
    blank: bool
    number: int | None
    main_text: str | None
