import discord
import asyncio
from discord.ext import commands
from discord import app_commands

from classes.discordbot import DiscordBot
from views.tu_prefere import ModalTuPrefere
from classes.utils import COLORS


@app_commands.guild_only()
class Vote(commands.GroupCog, name="vote", group_name="vote", group_description="Pour gérer les votes !"):
    def __init__(self, bot: DiscordBot):
        self.bot = bot
    
    @app_commands.command(name="tu_prefere", description="Sondage 'tu prefere' entre 2 choix.")
    @app_commands.guild_only()
    async def tu_prefere(self, interaction: discord.Interaction):
        modal = ModalTuPrefere()
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        # Generate Embed
        dict_embed = {
            'title': 'Tu prefere',
            'color': COLORS['blue'],
            'fields': [
                {
                    'name': f':one: - {modal.choix_1}',
                    'value': '',
                    'inline': False
                },
                {
                    'name': f':two: - {modal.choix_2}',
                    'value': '',
                    'inline': False
                }
            ]
        }
        embed = discord.Embed.from_dict(dict_embed)
        
        message = await interaction.followup.send(embed=embed)
        await message.add_reaction('1️⃣')
        await message.add_reaction('2️⃣')


async def setup(bot: DiscordBot):
    await bot.add_cog(Vote(bot))
