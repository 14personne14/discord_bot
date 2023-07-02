import discord
from discord.ext import commands
from discord import app_commands

from classes.discordbot import DiscordBot
from views.persistence import PersistentView


class Coucou(commands.GroupCog, name="coucou", group_name="coucou", group_description="Pour faire coucou !"):
    def __init__(self, bot: DiscordBot):
        self.bot = bot

    @commands.command(name="coucou", description="Dire coucou", aliases=['cc'])
    async def coucou(self, ctx: commands.Context):
        await ctx.send("Coucou")
        
    @app_commands.command(name="persistance", description="Créé une vue persistante.")
    async def persistance(self, interaction: discord.Interaction):
        await interaction.response.send_message('Bonjour !', view=PersistentView())


async def setup(bot: DiscordBot):
    await bot.add_cog(Coucou(bot))
