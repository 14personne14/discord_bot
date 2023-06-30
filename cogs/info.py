import discord
import asyncio
from discord.ext import commands
from discord import app_commands

from classes.discordbot import DiscordBot
from classes.utils import COLORS
from typing import Optional


class Info(commands.GroupCog, name="info", group_name="info", group_description="Pour gérer les votes !"):
    def __init__(self, bot: DiscordBot):
        self.bot = bot

    @app_commands.command(name="server", description="Les informations du serveur.")
    @app_commands.guild_only()
    async def server_info(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1)

        server_name = interaction.guild.name

        nbr_members = interaction.guild.member_count

        nbr_roles = len(interaction.guild.roles) - 1

        channels = interaction.guild.channels
        nbr_txt_channels = 0
        nbr_voc_channels = 0
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                nbr_txt_channels += 1
            if isinstance(channel, discord.VoiceChannel):
                nbr_voc_channels += 1

        nbr_roles = len(interaction.guild.roles)

        owner = interaction.guild.owner.mention

        afk_channel = interaction.guild.afk_channel
        if isinstance(afk_channel, discord.VoiceChannel):
            afk_channel = afk_channel.mention
        else:
            afk_channel = '`non défini`'

        date_creation = interaction.guild.created_at

        url_server_image = interaction.guild.icon.url

        # Generate Embed
        dict_embed = {
            'title': f'Information Serveur',
            'description': f':white_small_square: Nom du serveur : **{server_name}**\n:white_small_square: **{nbr_members}** membres \n:white_small_square: **{nbr_txt_channels}** salons textuels \n:white_small_square: **{nbr_voc_channels}** salons vocaux \n:white_small_square: **{nbr_roles}** roles \n:white_small_square: {owner} est le propriétaire \n:white_small_square: Créé le **{date_creation.day}/{date_creation.month}/{date_creation.year}** \n:white_small_square: Salon AFK : {afk_channel}',
            'color': COLORS['white'],
            'thumbnail': {
                'url': url_server_image,
            }
        }
        embed = discord.Embed.from_dict(dict_embed)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="member", description="Les informations d'un membre.")
    @app_commands.describe(member='Les informations de qui ?')
    @app_commands.guild_only()
    async def member_info(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        await interaction.response.defer(thinking=True)
        await asyncio.sleep(1)

        if member == None:
            member = interaction.user
        
        avatar_url = member.avatar.url
        discriminator = member.discriminator
        if discriminator == 0: 
            discriminator = '`aucun`'
        else: 
            discriminator = f'**{discriminator}**'
        
        flags = member.public_flags.all()
        badge = ''
        if len(flags) > 0: 
            badge = ""
            for flag in flags: 
                name = str(flag).split('.')[1]
                badge += f'`{name}` '
        else: 
            badge = '`aucun`'

        # Generate Embed
        dict_embed = {
            'title': 'Information Membre',
            'description': f':white_small_square: Nom du membre : **{member.mention}**\n:white_small_square: Tag : {discriminator} \n\n:white_small_square: Badge(s) : {badge}',
            'color': COLORS['white'],
            'thumbnail': {
                'url': avatar_url,
            }
        }
        embed = discord.Embed.from_dict(dict_embed)
        
        await interaction.followup.send(embed=embed)


async def setup(bot: DiscordBot):
    await bot.add_cog(Info(bot))
