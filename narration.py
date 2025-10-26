import json
import asyncio
from pathlib import Path

from openai import OpenAI, AsyncOpenAI
from openai.types.responses import ParsedResponse

from helpers import digit_sorter, print_tts_cost
from models import Section, Page
from env_vars import OPENAI_API_KEY, RESPONSES_DIR, SECTIONS_PATH, TEMP_DIR, BOOK_DIR

MAX_SECTION_LENGTH = 2000

async def create_narration(text: str, output_path: Path, openai_client: AsyncOpenAI):
    response = await openai_client.audio.speech.with_raw_response.create(
        model="tts-1",
        voice="sage",
        response_format="wav",
        input=text
    )
    output_path.write_bytes(response.content)
    return True



async def main():
    section_list = [Section.model_validate(s) for s in json.loads(SECTIONS_PATH.read_text())]
    for s in section_list:
        (BOOK_DIR / f"section_{s.number}").mkdir(exist_ok=True)
        scan_index_rage = range(s.starting_scan_index, s.ending_scan_index + 1)

        combined_main_text = ""
        for i in scan_index_rage:
            response = ParsedResponse[Page].model_validate_json((RESPONSES_DIR / f"{i}.json").read_text())

            main_text = response.output_parsed.main_text
            if main_text:
                combined_main_text += 2*"\n" + main_text
        
        print(combined_main_text[:200])
        print_tts_cost(len_characters=len(combined_main_text))

        break

        lines = combined_main_text.split("\n\n")
        split_counter = 0
        new_split = ""
        text_splits: list[str] = []

        openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        for l in lines:
            potential_split = new_split + "\n\n" + l
            if len(potential_split) < MAX_SECTION_LENGTH:
                new_split = potential_split
            else:
                text_splits.append(new_split)
                new_split = l
                split_counter +=1

        openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        split_counter = 0
        async with asyncio.TaskGroup() as tg:
            for ts in text_splits:
                print(f"Starting up: {split_counter}")
                tg.create_task(
                    create_narration(
                        text=ts,
                        output_path=BOOK_DIR / f"section_{s.number}" / f"{split_counter}.wav",
                        openai_client=openai_client
                    )
                )
                split_counter += 1


        
        
if __name__ == "__main__":
    asyncio.run(main())