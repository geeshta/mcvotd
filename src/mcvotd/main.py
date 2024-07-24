from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import anyio
from mcvotd.votd import get_votd, say_votd, mock_votd
from dotenv import dotenv_values
from typing import cast
from mcvotd.votd_types import VOTDEnv

env = cast(VOTDEnv, dotenv_values(".env"))
env["RCON_PORT"] = int(env["RCON_PORT"])
env["BIBLE_VERSION_CODE"] = int(env["BIBLE_VERSION_CODE"])
print(env)

async def job():
    result = await get_votd(env["BIBLE_VERSION_CODE"])
    await say_votd(result, env["RCON_ADDR"], env["RCON_PORT"], env["RCON_PASSWORD"])
    # await mock_votd(result)

async def main():

    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, IntervalTrigger(seconds=10))
    scheduler.start()
    
    await anyio.sleep_forever()

if __name__ == "__main__":
    anyio.run(main)