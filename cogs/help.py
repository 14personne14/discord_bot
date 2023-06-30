import discord
import asyncio
from discord.ext import commands
from discord import app_commands

from classes.discordbot import DiscordBot
from classes.utils import COLORS
from typing import Optional


class Help(commands.Cog, name="help"):
    def __init__(self, bot: DiscordBot):
        self.bot = bot
        self._original_help_command = bot.help_command

        bot.remove_command('help')

    @app_commands.command(name="help", description="Afficher l'aide.")
    async def help_command(self, interaction: discord.Interaction, command: Optional[str] = None):
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1)
        
        ctx = await self.bot.get_context(interaction)
        await self.send_help(ctx, command)

    @commands.command(name="help", description="Afficher l'aide.")
    async def help(self, ctx: commands.Context, command: Optional[str] = None):
        await self.send_help(ctx, command)

    async def send_help(self, ctx: commands.Context, command: Optional[str]):
        await ctx.send(embed=await self.generate_help_embed(command))

    async def generate_help_embed(self, command: Optional[str]) -> discord.Embed:
        list_commands_prefix = list(self.bot.commands)
        list_tree_commands = self.bot.tree.get_commands()
        
        # Extract liste of app commands
        list_app_commands = []
        for element in list_tree_commands: 
            if isinstance(element, discord.app_commands.Command): 
                list_app_commands.append(element)
            elif isinstance(element, discord.app_commands.Group): 
                for command in element.commands: 
                    list_app_commands.append(command)
        
        # Sort commands
        list_commands_prefix.sort(key=lambda x: x.name, reverse=False)
        list_app_commands.sort(key=lambda x: x.name, reverse=False)
        
        # Generate Embed
        dict_embed = {
            'description': "",
            "color": COLORS['yellow'],
        }
        
        dict_embed['description'] += f"\n## Commande Prefixe"
        for command in list_commands_prefix:
            dict_embed['description'] += f"\n:white_small_square: **{command.name}** - {command.description}"
        
        dict_embed['description'] += f"\n## Commande Slash"
        for command in list_app_commands:
            dict_embed['description'] += f"\n:white_small_square: **{command.name}** - {command.description}"
        
        return discord.Embed.from_dict(dict_embed)


async def setup(bot: DiscordBot):
    await bot.add_cog(Help(bot))
