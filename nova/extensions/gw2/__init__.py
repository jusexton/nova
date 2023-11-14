from typing import Final, Optional

import discord
from discord import ApplicationContext, Attachment
from discord.ext import commands

from nova import Nova
from nova.extensions.gw2.report import ReportClient, format_report
from nova.extensions.gw2.team import TeamService, format_team, RoleSelectTeamView, SimpleTeamView
from nova.extensions.gw2.types import Team, EventType

EVENT_CHOICES: Final[list[str]] = [event_type for event_type in EventType]


class GuildWars2(commands.Cog):
    """
    Cog providing guild wars 2 functionality.
    """

    def __init__(self):
        self.team_service = TeamService()

    @discord.slash_command(name='create-dps-report', description='Creates a DPS report from provided arcdps log file.')
    async def create_dps_report(self, ctx: ApplicationContext, attachment: Attachment):
        content = await attachment.read()
        async with ReportClient() as report_client:
            new_report = await report_client.upload(attachment.filename, content)
            message = format_report(new_report)
            await ctx.respond(message)

    @discord.slash_command(name='create-team', description='Facilitates the creation of a team.')
    async def create_team(
        self,
        ctx: ApplicationContext,
        event_type: discord.Option(str, choices=EVENT_CHOICES),
        role_selection: Optional[bool]
    ):
        new_team = self.team_service.create_team(event_type, role_selection)
        message = format_team(new_team)
        view_type = RoleSelectTeamView if role_selection else SimpleTeamView
        view = view_type(new_team, self.team_service)
        await ctx.respond(message, view=view)


def setup(bot: Nova):
    cog = GuildWars2()
    bot.add_cog(cog)
