import logging

import discord
from discord import ApplicationContext, Attachment
from discord.ext import commands

from nova.report import ReportClient, format_report

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)
report_client = ReportClient()


@bot.slash_command(name='create-dps-report', description='Creates a DPS report from provided arcdps log.')
async def create_dps_report(ctx: ApplicationContext, attachment: Attachment):
    content = await attachment.read()
    report = await report_client.upload(attachment.filename, content)
    message = format_report(report)
    await ctx.respond(message)


if __name__ == '__main__':
    bot.run('MTE2MzkyMzAyNTM1NjM5ODY2Mg.GvTwYX.WDUlUYej7JhkJ5oADJySSYRLltQlrUJIIgPr-Y')
