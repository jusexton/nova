from typing import Union

import aiohttp
import discord
import pydantic
from discord import ApplicationContext, Attachment
from discord.ext import commands
from pydantic import Field

from nova.core.util import SessionContextManager


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


UploadResult = Union[Report, str]


class ReportClient(SessionContextManager):
    """
    HTTP client used to interface with https://dps.report/api.
    """

    async def upload(self, name: str, content: bytes, anonymous: bool = False) -> UploadResult:
        """
        Uploads file content to the dps.report API.

        :param name: The filename that will be attached to the uploaded content.
        :param content: File content that will be uploaded.
        :param anonymous: Whether the report should be generated with anonymous player names.
        :return: The created report
        """

        form = aiohttp.FormData()
        form.add_field('json', '1')
        form.add_field('anonymous', str(anonymous))
        form.add_field('file', filename=name, value=content)

        async with self._session.post('https://dps.report/uploadContent', data=form) as response:
            data = await response.json()
            return data['error'] if data['error'] else Report(**data)


def format_duration(duration: float) -> str:
    minutes, seconds = divmod(int(duration), 60)
    minute_desc = 'minutes' if minutes != 1 else 'minute'
    second_desc = 'seconds' if seconds != 1 else 'second'
    return f'**{minutes}** {minute_desc} and **{seconds}** {second_desc}'


def format_report(report: Report) -> str:
    encounter = report.encounter
    duration = format_duration(encounter.duration)
    status = ':white_check_mark:' if encounter.success else ':x:'
    players = '\n'.join(
        f':crossed_swords: {player.display_name}'
        for player in report.players.values()
    )

    return (
        f'## Report\n'
        f'The full published report can be found here {report.permalink}.\n'
        '### Encounter\n'
        f'Name: {encounter.boss}\n'
        f'Status: {status}\n'
        f'Duration: {duration}\n'
        '### Players\n'
        f'{players}'
    )


class GuildWars2(commands.Cog):
    """
    Cog providing guild wars 2 functionality.
    """

    @discord.slash_command(name='create-dps-report', description='Creates a DPS report from provided arcdps log file.')
    async def create_dps_report(self, ctx: ApplicationContext, attachment: Attachment):
        content = await attachment.read()
        async with ReportClient() as client:
            report = await client.upload(attachment.filename, content)
            message = format_report(report)
            await ctx.respond(message)
