from discord import Intents
from discord.ext import commands

from nova.core import NovaCore
from nova.extensions.gw2 import GuildWars2
from nova.extensions.poll import Poll


class Nova(commands.Bot):
    def __init__(self, intents: Intents):
        super().__init__(intents=intents)

        self.add_cog(NovaCore())
        self.add_cog(GuildWars2())
        self.add_cog(Poll())
