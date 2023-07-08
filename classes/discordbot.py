import discord
from datetime import datetime
from discord import __version__ as discord_version
from discord.ext import commands
from logging import Logger
from logging import INFO
from classes.database import Database
from os import getenv
from views.persistence import PersistentView


class DiscordBot(commands.Bot):
    """A Subclass of `commands.Bot` to do more things."""

    def __init__(self, data):
        """Initialise le bot

        Raises:
            ValueError: _description_
        """
        
        self.data = data
        self.start_time = datetime.now()
        self.database = Database(
            host='seb_mysql_db',
            username='eloilag',
            password=getenv('MDP_DATABASE'),
            database_name='eloilag', 
            log=self.log
        )

        super().__init__(
            command_prefix=commands.when_mentioned_or(self.data["default_prefix"]),
            activity=discord.Game(name=self.data["default_activity"]),
            intents=discord.Intents.all(),
            case_insensitive=True,
            max_messages=2500,
            status=discord.Status.online,
        )

    def log(self, message: str, name: str, level: int = INFO, **kwargs):
        """Log a message to the console and the log file.

        Args:
            message (str): The message to log.
            name (str): The name of the logger.
            level (int, optional): The level of the log message. Defaults to INFO.
        """

        self.logger.name = name
        self.logger.log(level=level, msg=message, **kwargs)

    async def on_ready(self):
        """When the bot is ready. 
        """

        self.log(
            message=f"Bot is ready | Logged as: {self.user} | Version discord.py: {discord_version} | Number_Guilds: {len(self.guilds)} | Number_Users: {len(self.users)} | Connected to database : {print(self.database.is_connected())}",
            name="discord.on_ready"
        )

    async def setup_hook(self):
        """Retrieve the bot's application info.
        """

        self.appinfo = await self.application_info()
        self.add_view(PersistentView())
