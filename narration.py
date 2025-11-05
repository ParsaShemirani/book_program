import asyncio
import subprocess
from tempfile import TemporaryDirectory
from pathlib import Path

from openai import AsyncOpenAI

from env_vars import OPENAI_API_KEY
from helpers import get_sorted_files

TARGET_SPLIT_LENGTH = 500


openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def generate_text_splits_dir(scan_dir_path: Path):
    main_text = (scan_dir_path / "main_text.md").read_text()
    lines = main_text.split("\n\n")

    text_splits: list[str] = [""]
    for i, l in enumerate(lines):
        last_split = text_splits[-1]
        candidate = last_split + "\n\n" + l
        if len(candidate) > TARGET_SPLIT_LENGTH:
            text_splits.append(l)
        else:
            text_splits[-1] += l

    text_splits_dir = scan_dir_path / "text_splits"
    text_splits_dir.mkdir()

    text_splits = [ts for ts in text_splits if ts.strip()]
    for i, ts in enumerate(text_splits, start=1):
        output_path = text_splits_dir / f"{i}.md"
        output_path.write_text(ts) 

async def generate_narration_response(text: str) -> bytes:
    response = await openai_client.audio.speech.with_raw_response.create(
        model="tts-1", voice="sage", response_format="wav", input=text
    )
    return response.content


async def generate_and_save_narration(text: str, output_path: Path):
    wav_bytes = await generate_narration_response(text)
    output_path.write_bytes(wav_bytes)

async def generate_narration_splits_dir(scan_path_dir: Path):
    text_split_paths = get_sorted_files(scan_path_dir / "text_splits")

    narration_splits_dir = scan_path_dir / "narration_splits"
    narration_splits_dir.mkdir()

    async with asyncio.TaskGroup() as tg:
        for tsp in text_split_paths:
            tg.create_task(
                generate_and_save_narration(tsp.read_text(), narration_splits_dir / f"{tsp.stem}.wav") 
            )

def generate_narration(scan_path_dir: Path):
    narration_split_paths = get_sorted_files(scan_path_dir / "narration_splits")

    concat_list_path = scan_path_dir / "concat_list.txt"

    for nsp in narration_split_paths:
        with open(concat_list_path, 'a') as f:
            f.write(f"file '{str(nsp)}'\n")

    narration_path = scan_path_dir / "narration.wav"
    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(concat_list_path), "-c", "copy", str(narration_path)]

    subprocess.run(cmd)
  


async def split_narrate_save_text(file_path: Path):
        concat_list_path = tempdir_path / "jamies.txt"
        concat_list_str = ""
        for f in wav_files:
            concat_list_str += f"file '{str(f)}'\n"
        concat_list_path.write_text(concat_list_str)

        output_file_path = file_path.parent / f"{file_path.stem}.wav"

        cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(concat_list_path), "-c", "copy", str(output_file_path)]
        subprocess.run(cmd)


