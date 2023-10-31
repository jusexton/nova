import logging

import discord

from nova import Nova, config

logging.basicConfig(level=logging.INFO)

cfg = config.load()
all_intents = discord.Intents.all()
nova = Nova(cfg, all_intents)
nova.run(cfg.token)
