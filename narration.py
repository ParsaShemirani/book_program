import asyncio
import subprocess
from tempfile import TemporaryDirectory
from pathlib import Path

from openai import AsyncOpenAI

from env_vars import OPENAI_API_KEY
from helpers import get_sorted_files

TARGET_SPLIT_LENGTH = 500


openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)




async def narrate_text(text: str) -> bytes:
    response = await openai_client.audio.speech.with_raw_response.create(
        model="tts-1", voice="sage", response_format="wav", input=text
    )
    return response.content


async def narrate_and_save_text(text: str, output_path: Path):
    try:
        wav_bytes = await narrate_text(text=text)
        output_path.write_bytes(wav_bytes)
    except Exception as e:
        print(f"FAILIURE FOR PATH {output_path}: {e}")



async def split_narrate_save_text(file_path: Path):
    text = file_path.read_text()
    lines = text.split("\n\n")
    text_splits: list[str] = [""]

    for i, l in enumerate(lines):
        last_split = text_splits[-1]
        candidate = last_split + "\n\n" + l
        if len(candidate) > TARGET_SPLIT_LENGTH:
            text_splits.append(l)
        else:
            text_splits[-1] += l

    text_splits = [ts for ts in text_splits if ts.strip()]

    with TemporaryDirectory() as tempdir:
        async with asyncio.TaskGroup() as tg:
            tempdir_path = Path(tempdir)
            for i, ts in enumerate(text_splits, start=1):
                tg.create_task(
                    narrate_and_save_text(
                        text=ts,
                        output_path=tempdir_path / f"{i}.wav"
                    )
                )
        wav_files = get_sorted_files(dir_path = tempdir_path)
        concat_list_path = tempdir_path / "jamies.txt"
        concat_list_str = ""
        for f in wav_files:
            concat_list_str += f"file '{str(f)}'\n"
        concat_list_path.write_text(concat_list_str)

        output_file_path = file_path.parent / f"{file_path.stem}.wav"

        cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(concat_list_path), "-c", "copy", str(output_file_path)]
        subprocess.run(cmd)


