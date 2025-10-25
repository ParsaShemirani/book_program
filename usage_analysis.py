from helpers import get_extractions
from env_vars import RESPONSE_DIR


def tokens_to_dollars(token_count: int, kind: str) -> float:
    rates = {"input": 0.250 / 1000000, "output": 2 / 1000000}
    if kind not in rates:
        raise ValueError("Unknown kind provided")
    return token_count * rates[kind]


def get_usage_stats() -> str:
    total_input_tokens = 0
    total_output_tokens = 0
    usage_stats = ""

    extractions = get_extractions()
    for e in extractions:
        input_tokens = e.response.usage.input_tokens
        output_tokens = e.response.usage.output_tokens

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        usage_stats += f"Extraction {e.file_path.stem} | Input: {input_tokens} | Output: {output_tokens}\n\n"

    usage_stats += f"Total input tokens: {total_input_tokens} | Total output tokens: {total_output_tokens}\n\n"

    total_input_cost = tokens_to_dollars(token_count=total_input_tokens, kind="input")
    total_output_cost = tokens_to_dollars(
        token_count=total_output_tokens, kind="output"
    )
    usage_stats += f"Total input cost: ${total_input_cost} | Total output cost: ${total_output_cost}\n"
    usage_stats += f"Total cost: ${total_input_cost + total_output_cost}\n"
    return usage_stats


def main() -> None:
    usage_stats = get_usage_stats()
    usage_stats_output_path = RESPONSE_DIR / "other" / "usage_stats.txt"
    usage_stats_output_path.write_text(usage_stats)


if __name__ == "__main__":
    main()
