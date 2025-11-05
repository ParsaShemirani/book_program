from pydantic import BaseModel

class Page(BaseModel):
    main_text: str | None

class ModelPricing(BaseModel):
    input_cost_per_1M: float
    output_cost_per_1M: float
