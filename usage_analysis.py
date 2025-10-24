from pathlib import Path
from openai.types.responses.parsed_response import ParsedResponse

from extractor import PageExtraction
from env_vars import EXTRACTION_RESPONSE_DIR

total_input_tokens = 0
total_output_tokens = 0


def is_integer_stem(file_path: Path) -> bool:
    try:
        int(file_path.stem)
        return True
    except ValueError:
        return False
    
def tokens_to_dollars(token_count: int, kind: str):
    rates = {
        "input": 0.250 / 1000000,
        "output": 2 / 1000000
    }
    if kind not in rates:
        raise ValueError("Unknown kind provided")
    return token_count * rates[kind]

file_paths = [
    f
    for f in EXTRACTION_RESPONSE_DIR.glob("*")
    if not f.name.startswith(".") and f.is_file() and is_integer_stem(f)
]
file_paths_sorted = sorted(file_paths, key=lambda p: int(p.stem))

responses: list[tuple[Path, ParsedResponse[PageExtraction]]] = []
for f in file_paths_sorted:
    response_string = f.read_text()
    r = ParsedResponse.model_validate_json(json_data=response_string)
    responses.append((f, r))

total_input_tokens = 0
total_output_tokens = 0
usage_stats = ""

for f, r in responses:
    input_tokens = r.usage.input_tokens
    output_tokens = r.usage.output_tokens

    total_input_tokens += input_tokens
    total_output_tokens += output_tokens
    usage_stats += f"Extraction {f.stem} | Input: {input_tokens} | Output: {output_tokens}\n\n"

usage_stats += f"Total input tokens: {total_input_tokens} | Total output tokens: {total_output_tokens}\n\n"

total_input_cost = tokens_to_dollars(token_count=total_input_tokens, kind="input")
total_output_cost = tokens_to_dollars(token_count=total_output_tokens, kind="output")
usage_stats += f"Total input cost: ${total_input_cost} | Total output cost: ${total_output_cost}\n"
usage_stats += f"Total cost: ${total_input_cost + total_output_cost}\n"

usage_stats_output_path = EXTRACTION_RESPONSE_DIR / "usage_stats.txt"
usage_stats_output_path.write_text(usage_stats)