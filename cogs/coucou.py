import discord
from discord.ext import commands
from discord import app_commands

from classes.discordbot import DiscordBot


class Coucou(commands.GroupCog, name="coucou", group_name="coucou", group_description="Pour faire coucou !"):
    def __init__(self, bot: DiscordBot):
        self.bot = bot

    @commands.command(name="coucou", description="Dire coucou", aliases=['cc'])
    async def coucou(self, ctx: commands.Context):
        await ctx.send("Coucou")


async def setup(bot: DiscordBot):
    await bot.add_cog(Coucou(bot))
