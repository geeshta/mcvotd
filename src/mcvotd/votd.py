from httpx import AsyncClient
from aiomcrcon import Client
from xml.etree import ElementTree
from mcvotd.votd_types import VOTDict, VOTDKey
import html
import anyio


def extract_el(root: ElementTree.Element, key: VOTDKey) -> str:
    element = root.find(key)
    text = "" if element is None else element.text
    return "" if text is None else html.unescape(text.strip())

async def get_votd(version_num: int) -> VOTDict:
    async with AsyncClient() as client:
        res = await client.get(f"https://www.biblegateway.com/votd/get/?version={version_num}")
        root = ElementTree.fromstring(res.text)

        day = extract_el(root, "day")
        month = extract_el(root, "month")
        year = extract_el(root, "year")

        return {
            "content": extract_el(root, "content"),
            "display_ref": extract_el(root, "display_ref"),
            "version": extract_el(root, "version"),
            "date": f"{day}.{month}.{year}"
        }


async def say_votd(votd: VOTDict, addr: str, port: int, password: str) -> None:
    async with Client(addr, port, password) as client:
        await client.send_cmd(f"/say Verš pro den {votd['date']}:")
        await anyio.sleep(2)
        await client.send_cmd(f"/say {votd['content']}")
        await anyio.sleep(1)
        await client.send_cmd(f"/say {votd['display_ref']}, {votd['version']}")

async def mock_votd(votd: VOTDict) -> None:
        print(f"/say Verš pro den {votd['date']}:")
        await anyio.sleep(2)
        print(f"/say {votd['content']}")
        await anyio.sleep(1)
        print(f"/say {votd['display_ref']}, {votd['version']}")