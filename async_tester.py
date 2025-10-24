import asyncio

from openai import AsyncOpenAI

from env_vars import OPENAI_API_KEY

sample_list = ["Hydro flask", "Apple", "Stanley", "MSR", "Panasonic"]

async def ai_response(openai_client: AsyncOpenAI, brand: str):
    print(f"STARTING UP FOR: {brand}")
    response = await openai_client.responses.create(
        model="gpt-5-nano",
        instructions="Write a 2 sentence history on how the following company was created",
        input=brand
    )
    print(f"RESPONSE DONE FOR: {brand}")
    print(response.output_text)
    print(10*"\n")





async def task_group_method():
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    async with asyncio.TaskGroup() as tg:
        for brand in sample_list:
            task = tg.create_task(ai_response(openai_client=client, brand=brand))

async def create_task_method():
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    tasks = []
    for brand in sample_list:
        task = asyncio.create_task(ai_response(openai_client=client, brand=brand))
        tasks.append(task)
    await asyncio.gather(*tasks)


"""
import asyncio

async def worker(name, sem):
    async with sem:  # acquire and release automatically
        print(f"{name} is working...")
        await asyncio.sleep(1)
        print(f"{name} finished.")

async def main():
    sem = asyncio.Semaphore(2)  # allow only 2 concurrent workers

    tasks = [worker(f"Worker {i}", sem) for i in range(5)]
    await asyncio.gather(*tasks)

asyncio.run(main())


"""