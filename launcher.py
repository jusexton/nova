import logging

import discord

from nova import Nova

logging.basicConfig(level=logging.INFO)

all_intents = discord.Intents.all()
nova = Nova(all_intents)
nova.run('token')
