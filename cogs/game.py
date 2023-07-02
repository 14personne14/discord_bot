import discord
import asyncio
from discord.ext import commands
from discord import app_commands

from classes.discordbot import DiscordBot
from classes.utils import COLORS
from typing import Optional


class Game(commands.Cog, name="game"):
    def __init__(self, bot: DiscordBot):
        self.bot = bot

    @app_commands.command(name="game", description="Jouer à un jeu cool.")
    @app_commands.guild_only()
    async def game(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1)


async def setup(bot: DiscordBot):
    await bot.add_cog(Game(bot))
