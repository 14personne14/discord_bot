import discord
from discord.ext import commands
from discord import app_commands
from logging import ERROR, CRITICAL

from classes.discordbot import DiscordBot


class Errors(commands.Cog, name="errors"):
    """Errors handler."""

    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot
        self.default_error_message = "Une erreur est survenue !"

    @commands.Cog.listener()
    async def on_error(self, event: str, *args, **kwargs) -> None:
        """When there is an error."""

        self.bot.log(
            message=f"Unexpected Internal Error: (event) {event}, (args) {args}, (kwargs) {kwargs}.",
            name="discord.on_error",
            level=CRITICAL
        )

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
    #     """When there is an error in a command."""



async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(Errors(bot))
