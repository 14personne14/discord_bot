import discord
from datetime import datetime
from discord import __version__ as discord_version
from discord.ext import commands
from logging import Logger
from logging import INFO


class DiscordBot(commands.Bot):
    """A Subclass of `commands.Bot` to do more things."""

    def __init__(self, data) -> None:
        """Initialise le bot

        Raises:
            ValueError: _description_
        """
        self.data = data

        self.uptime: datetime = datetime.now()
        """Bot's uptime."""

        super().__init__(
            command_prefix=self.data["default_prefix"],
            activity=discord.Game(name=self.data["default_activity"]),
            intents=discord.Intents.all(),
            case_insensitive=True,
            max_messages=2500,
            status=discord.Status.online,
        )

    def log(self, message: str, name: str, level: int = INFO, **kwargs) -> None:
        """Log a message to the console and the log file.

        Args:
            message (str): The message to log.
            name (str): The name of the logger.
            level (int, optional): The level of the log message. Defaults to INFO.
        """

        logger: Logger
        self.logger.name = name
        self.logger.log(level=level, msg=message, **kwargs)

    async def on_ready(self) -> None:
        """When the bot is ready. 
        """

        self.log(
            message=f"Logged as: {self.user} | Version: discord.py{discord_version} | Number_Guilds: {len(self.guilds)} | Number_Users: {len(self.users)}", name="discord.on_ready")

    async def setup_hook(self) -> None:
        """Retrieve the bot's application info.
        """

        self.appinfo = await self.application_info()
        """Application info for the bot provided by Discord."""
