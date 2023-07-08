# Discord
import discord
from discord.ext import commands
from discord import app_commands

# Other
import sys, os
from logging import ERROR, CRITICAL
from typing import Any

# My import 
from classes.utils import COLORS
from classes.discordbot import DiscordBot


class Errors(commands.Cog, name="errors"):
    """Errors handler."""

    def __init__(self, bot: DiscordBot):
        self.bot = bot
        self.default_error_message = "Une erreur est survenue !"
    
    async def send_error(self):
        pass

    @commands.Cog.listener('on_error')
    async def on_error(self, event: str, *args, **kwargs):
        """When there is an error."""

        self.bot.log(
            message=f"Unexpected Internal Error: (event) {event}, (args) {args}, (kwargs) {kwargs}.",
            name="discord.on_error",
            level=CRITICAL
        )

    @commands.Cog.listener('on_command_error')
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """When there is an error in a command."""
    
        self.bot.log(
            message=f"Unexepted Internal Command Error in '{ctx.command.name}' \n{error}",
            name="discord.on_command_error",
            level=CRITICAL
        )
        
        # Generate Embed
        dict_embed = {
            'description': f"❌ Une erreur est survenue dans la commande '{ctx.command.name}' ! \n\n```\n{error}\n``` ",
            'color': COLORS['red'],
        }
        embed = discord.Embed.from_dict(dict_embed)
        await ctx.send(embed=embed)
    
    #@commands.Cog.listener("on_app_command_error")
    async def on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
        """When there is an error in a slash command"""
        
        print('error found')
        
        """
        self.bot.log(
            message=f"Unexepted Internal Command Error \n{error}",
            name="discord.on_command_error",
            level=CRITICAL
        )
        
        # Generate Embed
        dict_embed = {
            'description': f'❌ Une erreur est survenue ! \n\n```\n{error}\n``` ',
            'color': COLORS['red'],
        }
        embed = discord.Embed.from_dict(dict_embed)
        await interaction.edit_original_response(embed=embed)
        """
    
    @commands.Cog.listener("on_modal_error")
    async def on_modal_error(self, interaction: discord.Interaction, error: Exception):
        """When there is an error in a Modal"""
        pass
    
    @commands.Cog.listener("on_view_error")
    async def on_view_error(self, interaction: discord.Interaction, error: Exception, item: Any) -> None:
        """When there is an error in a View"""
        pass



async def setup(bot: DiscordBot):
    await bot.add_cog(Errors(bot))
