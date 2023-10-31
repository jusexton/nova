from discord import Intents
from discord.ext import commands

from nova.config import NovaConfiguration
from nova.core import NovaCore


class Nova(commands.Bot):
    def __init__(self, cfg: NovaConfiguration, intents: Intents):
        super().__init__(intents=intents)
        self.cfg = cfg

        self.add_cog(NovaCore())
        for extension in cfg.extensions:
            name = extension if isinstance(extension, str) else extension.name
            self.load_extension(f"extensions.{name}")
