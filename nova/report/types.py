import pydantic
from pydantic import Field


class Player(pydantic.BaseModel):
    display_name: str
    profession: int
    elite_spec: int


class Encounter(pydantic.BaseModel):
    success: bool
    duration: float
    boss: str
    is_challenge_mode: bool = Field(..., alias='isCm')


class Report(pydantic.BaseModel):
    id: str
    permalink: str
    players: dict[str, Player]
    encounter: Encounter
