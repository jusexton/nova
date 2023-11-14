import discord

from nova.config import NovaConfiguration
from nova.core import NovaCore


class Nova(discord.Bot):
    def __init__(self, cfg: NovaConfiguration):
        super().__init__()
        self.cfg = cfg

        self.add_cog(NovaCore())
        for extension in cfg.extensions:
            name = extension if isinstance(extension, str) else extension.name
            self.load_extension(f'nova.extensions.{name}')
