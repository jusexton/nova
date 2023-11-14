from enum import StrEnum
from typing import Optional

import pydantic
from pydantic import Field


class EventType(StrEnum):
    DUNGEON_OR_FRACTALS = 'Dungeon/Fractals'
    RAID_OR_STRIKES = 'Raid/Strikes'

    def member_limit(self) -> int:
        match self:
            case EventType.DUNGEON_OR_FRACTALS:
                return 5
            case EventType.RAID_OR_STRIKES:
                return 10


class TeamMember(pydantic.BaseModel):
    name: str
    role: Optional[str] = None


class Team(pydantic.BaseModel):
    id: str
    event_type: EventType
    role_selection: Optional[bool] = False
    members: list[TeamMember] = []

    @pydantic.computed_field()
    def count(self) -> int:
        match self.event_type:
            case EventType.DUNGEON_OR_FRACTALS:
                return 5
            case EventType.RAID_OR_STRIKES:
                return 10

    def contains(self, member_name: str) -> bool:
        member_names = [member.name for member in self.members]
        return member_name in member_names


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
