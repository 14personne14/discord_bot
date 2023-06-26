import platform
import asyncio
from logging import DEBUG, INFO, getLogger, Formatter, FileHandler, StreamHandler, Logger
from os import listdir
from os.path import splitext, join
from json import load as load_json
from classes.discordbot import DiscordBot


def extract_json(path_file: str) -> dict:
    """Extract data from json file

    Returns:
        dict: The data of json file
    """
    
    with open(path_file, "r") as file:
        return load_json(file)


def get_list_cogs(path_folder: str) -> list[str]:
    """Get the list of all cogs

    Args:
        path_folder (str): The path of the cogs folders 

    Returns:
        list[str]: The list of all cogs name 
    """
    
    list_cogs = []
    for filename in listdir(path_folder):
        if filename.endswith('.py'):
            list_cogs.append(f"cogs.{filename[:-3]}")
    return list_cogs


async def cogs_manager(bot: DiscordBot, mode: str, cogs: list[str]) -> None:
    """Manage a cog (load, realod, unload)

    Args:
        bot (DiscordBot): The bot 
        mode (str): What to do at cog (load, reload or unload)
        cogs (list[str]): The list of cogs to apply mode

    Raises:
        ValueError: The mode is not valid 
        err: Error for load, unload or reload
    """
    
    for cog in cogs:
        try:
            if mode == "unload":
                await bot.unload_extension(cog)
            elif mode == "load":
                await bot.load_extension(cog)
            elif mode == "reload":
                await bot.reload_extension(cog)
            else:
                raise ValueError("Invalid mode.")
            bot.log(f"Cog {cog} {mode}ed.", name="classes.utils", level=DEBUG)
        except Exception as err:
            raise err


def clean_close() -> None:
    """Avoid Windows EventLoopPolicy Error
    """
    
    if platform.system().lower() == 'windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def set_logging(file_level: int = DEBUG, console_level: int = INFO, filename: str = "./discord.log") -> tuple[Logger, StreamHandler]:
    """Sets up logging for the bot.

    Args:
        file_level (int, optional): The level of what to save in the file. Defaults to DEBUG.
        console_level (int, optional): The level of what to show in the console. Defaults to INFO.
        filename (str, optional): The name of the file to save the logs. Defaults to "./discord.log".

    Returns:
        tuple[Logger, StreamHandler]: The logger and the console handler. 
    """

    logger = getLogger("discord")  # discord.py logger
    logger.setLevel(DEBUG)
    log_formatter = Formatter(
        fmt="[{asctime}] [{levelname:<8}] {name}: {message}", datefmt="%Y-%m-%d %H:%M:%S", style="{")

    # File-logs
    file_handler = FileHandler(filename=filename, encoding="utf-8", mode='w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(file_level)
    logger.addHandler(file_handler)

    # Console-logs
    console_handler = StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(console_level)
    logger.addHandler(console_handler)

    return logger, console_handler
