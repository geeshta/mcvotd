from typing import TypedDict, Literal

type VOTDKey = Literal["content", "display_ref", "version", "day", "month", "year"]

class VOTDict(TypedDict):
    content: str
    display_ref: str
    version: str
    date: str

class VOTDEnv(TypedDict):
    RCON_ADDR: str
    RCON_PORT: int
    RCON_PASSWORD: str
    BIBLE_VERSION_CODE: int

