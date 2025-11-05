import re
import functools
from pathlib import Path

from PIL import Image
from openai.types.responses import Response

from models import Page, ModelPricing


def digit_sorter(p: Path):
    stem = p.stem
    digits = re.findall(r"\d+", stem)
    if digits:
        return int(digits[-1])
    else:
        raise (
            ValueError(
                f"Filename does not contain digits to index by. Filename: {str(p)}"
            )
        )


def get_sorted_files(dir_path: Path) -> list[Path] | None:
    file_paths = sorted(
        [f for f in dir_path.glob("*") if not f.name.startswith(".") and f.is_file()],
        key=digit_sorter,
    )
    if file_paths:
        return file_paths
    else:
        return None


def rotate_images(dir_path: Path, degrees: float):
    file_paths = get_sorted_files(dir_path=dir_path)
    if not file_paths:
        return None

    for f in file_paths:
        image = Image.open(f)
        image_rotated = image.rotate(angle=degrees, expand=True)
        image_rotated.save(f)


def calculate_response_cost(response: Response) -> float:
    pricing: dict[str, ModelPricing] = {
        "gpt-5-nano": ModelPricing(input_cost_per_1M=0.05, output_cost_per_1M=0.40),
        "gpt-5-mini": ModelPricing(input_cost_per_1M=0.25, output_cost_per_1M=2.00),
        "gpt-5": ModelPricing(input_cost_per_1M=1.25, output_cost_per_1M=10),
    }
    model_key = next((key for key in pricing if key in response.model), None)
    if model_key is None:
        raise KeyError(f"Pricing data not available for model: {response.model}")
    model_pricing = pricing[model_key]

    input_cost = response.usage.input_tokens * (
        model_pricing.input_cost_per_1M / 1000000
    )
    output_cost = response.usage.output_tokens * (
        model_pricing.output_cost_per_1M / 1000000
    )
    total_cost = input_cost + output_cost
    return total_cost
