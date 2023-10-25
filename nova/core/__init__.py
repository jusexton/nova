import discord
from discord import ApplicationContext, Embed, EmbedField
from discord.ext import commands


class NovaCore(commands.Cog):
    @discord.slash_command(name='ages', description='Displays the severs age along with all its members.')
    async def ages(self, ctx: ApplicationContext):
        names, joined_dates = [], []
        for member in sorted(ctx.guild.members, key=lambda m: m.joined_at):
            names.append(f'**{member.name}**')
            joined_dates.append(f'{member.joined_at:%b %d, %Y}')

        embed = Embed(
            title='Ages',
            description=f'**Server created:** {ctx.guild.created_at:%b %d, %Y}\n',
            fields=[
                EmbedField(name='Name', value='\n'.join(names), inline=True),
                EmbedField(name='Joined', value='\n'.join(joined_dates), inline=True)
            ]
        )
        await ctx.respond(embed=embed)
