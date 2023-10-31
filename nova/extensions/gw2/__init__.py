import discord
from discord import ApplicationContext, Attachment
from discord.ext import commands

from nova import Nova
from nova.extensions.gw2.client import ReportClient
from nova.extensions.gw2.format import ReportFormatter


class GuildWars2(commands.Cog):
    """
    Cog providing guild wars 2 functionality.
    """

    def __init__(self):
        self.report_formatter = ReportFormatter()

    @discord.slash_command(name='create-dps-report', description='Creates a DPS report from provided arcdps log file.')
    async def create_dps_report(self, ctx: ApplicationContext, attachment: Attachment):
        content = await attachment.read()
        async with ReportClient() as report_client:
            report = await report_client.upload(attachment.filename, content)
            message = self.report_formatter(report)
            await ctx.respond(message)


def setup(bot: Nova):
    cog = GuildWars2()
    bot.add_cog(cog)
