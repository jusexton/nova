import discord
from discord import ApplicationContext
from discord.ext import commands

from nova import Nova


class Poll(commands.Cog):
    """
    Cog providing poll creation functionality.
    """

    @discord.slash_command(name='poll', description='Creates a new poll.')
    async def poll(self, ctx: ApplicationContext, question: str):
        discord.Embed(
            title='Poll',
            description=question,
            fields=[
                discord.EmbedField(),
                discord.EmbedField()
            ]
        )


def setup(bot: Nova):
    cog = Poll()
    bot.add_cog(cog)
