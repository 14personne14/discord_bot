import discord

from discord.ext import commands
from discord import app_commands
from typing import Union

from classes.discordbot import DiscordBot


@app_commands.guild_only()
class TestDeNomBizarre(commands.GroupCog, name="me", group_name="me", group_description="Petite description du groupe !"):
    """
    Petite description du groupe 222 !

    Require intents: 
            - None

    Require bot permission:
            - None
    """

    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @app_commands.command(name="set", description="Set your own brief description of yourself !")
    @app_commands.describe(description="Your brief description of yourself.")
    @app_commands.guild_only()
    async def me(self, interaction: discord.Interaction, description: str) -> None:
        """Allows you to set or show a brief description of yourself."""
        await interaction.response.send_message(f"coucou c'est moi : {description}")
    
    
    @commands.command(name="coucou")
    @commands.is_owner()
    async def coucou_chef(self, ctx: commands.Context, message: str) -> None:
        """Unload a cog."""
        await ctx.send(f"- {message} !")


async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(TestDeNomBizarre(bot))
