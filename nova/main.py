import logging

import discord
from discord import ApplicationContext, Attachment, EmbedField, Embed
from discord.ext import commands

from nova.report import ReportClient, format_report

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)
report_client = ReportClient()


@bot.slash_command(name='create-dps-report', description='Creates a DPS report from provided arcdps log file.')
async def create_dps_report(ctx: ApplicationContext, attachment: Attachment):
    content = await attachment.read()
    report = await report_client.upload(attachment.filename, content)
    message = format_report(report)
    await ctx.respond(message)


@bot.slash_command(name='ages', description='Displays the severs age along with all its members.')
async def ages(ctx: ApplicationContext):
    guild_members = sorted(ctx.guild.members, key=lambda member: member.joined_at)
    embed = Embed(
        title='Ages',
        description=f'**Server created:** {ctx.guild.created_at:%b %d, %Y}\n',
        fields=[
            EmbedField(
                name='Name',
                value='\n'.join(f'**{member.name}**' for member in guild_members),
                inline=True
            ),
            EmbedField(
                name='Joined',
                value='\n'.join(f'{member.joined_at:%b %d, %Y}' for member in guild_members),
                inline=True
            )
        ]
    )
    await ctx.respond(embed=embed)


if __name__ == '__main__':
    bot.run('MTE2MzkyMzAyNTM1NjM5ODY2Mg.GvTwYX.WDUlUYej7JhkJ5oADJySSYRLltQlrUJIIgPr-Y')
