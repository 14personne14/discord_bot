from logging import DEBUG, INFO
from os import getenv
from dotenv import load_dotenv

from classes.discordbot import DiscordBot
from classes.utils import extract_json, get_list_cogs, clean_close, set_logging, cogs_manager


class Bot(DiscordBot):
    """The bot (client). 
    A Subclass of `DiscordBot`.
    """

    def __init__(self):
        data = extract_json('./config/bot.json')
        super().__init__(data)

    async def startup(self):
        """Sync application commands"""
        await self.wait_until_ready()

        list_synced = await self.tree.sync()
        self.log(
            message=f"Application commands synced (Number: {len(list_synced)})",
            name="discord.startup"
        )

    async def setup_hook(self):
        """Initialize the bot, prefixes, slash commands & cogs."""
        await super().setup_hook()

        # Cogs loader
        list_cogs = get_list_cogs('./cogs')
        await cogs_manager(self, "load", list_cogs)
        self.log(
            message=f"Cogs loaded (Number: {len(list_cogs)}): {', '.join(list_cogs)}",
            name="discord.setup_hook"
        )

        # Sync application commands
        self.loop.create_task(self.startup())


if __name__ == '__main__':
    clean_close()

    # Load '.env' file
    load_dotenv('.env')

    # Create the bot
    bot = Bot()
    bot.logger, streamHandler = set_logging(
        file_level=INFO,
        console_level=DEBUG,
        filename="./logs/discord.log"
    )
    bot.run(
        getenv('TOKEN'),
        reconnect=True,
        log_handler=streamHandler,
        log_level=INFO
    )
