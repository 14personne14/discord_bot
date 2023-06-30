import discord
import asyncio
from discord.ext import commands
from discord import app_commands

from classes.discordbot import DiscordBot
from views.tu_prefere import ModalTuPrefere
from classes.utils import COLORS, extract_json
from typing import Optional
from datetime import timedelta


@app_commands.guild_only()
class Moderation(commands.GroupCog, name="moderation", group_name="moderation", group_description="La modération pour les serveurs."):
    def __init__(self, bot: DiscordBot):
        self.bot = bot
    
    @app_commands.command(name="mute", description="Rendre muet un membre pendant un certain temps.")
    @app_commands.describe(member='Le membre à rendre muet.')
    @app_commands.rename(reason='raison')
    @app_commands.describe(reason='Pourquoi faut-il mute ce membre?')
    @app_commands.rename(days='jours')
    @app_commands.describe(days='Combien de jours?')
    @app_commands.rename(hours='heures')
    @app_commands.describe(hours="Combien d'heures?")
    @app_commands.describe(minutes='Combien de minutes?')
    @app_commands.rename(seconds='secondes')
    @app_commands.describe(seconds='Combien de secondes?')
    @app_commands.guild_only()
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "Aucune raison n'a été donnée.", days: Optional[int] = 0, hours: Optional[int] = 0, minutes: Optional[int] = 0, seconds: Optional[int] = 0):
        guild_id = str(interaction.guild.id)
        data = extract_json('./config/moderation.json')
        id_admin_role = data[guild_id]['admin']
        id_moderator_role = data[guild_id]['moderator']
        
        if (days == 0) and (hours == 0) and (minutes == 0) and (seconds == 0): 
            minutes = 1
        
        if not(interaction.user.get_role(id_admin_role) != None or interaction.user.get_role(id_moderator_role) != None): 
            dict_embed = {
                'description': f"❌ Vous n'avez pas les permissions necessaires pour réaliser cette commande !",
                'color': COLORS['red'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, ephemeral = True)

        elif not(days <= 27 and hours <= 24 and minutes <= 60 and seconds <= 60 and days >= 0 and hours >= 0 and minutes >= 0 and seconds >= 0): 
            dict_embed = {
                'description': f"❌ Vous avez entré des mauvaises valeurs !\n\n__Rappel:__ Vous ne devez pas dépasser 28 jours de mute !",
                'color': COLORS['red'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, ephemeral = True)
            
        elif interaction.user.id == member.id: 
            dict_embed = {
                'description': f"❌ Vous ne pouvez pas vous mute vous-même !\n\n*Vous êtes bête ou quoi ?*",
                'color': COLORS['red'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, ephemeral = True)
            
        elif member.bot: 
            dict_embed = {
                'description': f"❌ Vous ne pouvez pas mute un bot !\n\n*Bah non, c'est logique !*",
                'color': COLORS['red'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, ephemeral = True)
            
        elif member.guild_permissions.administrator: 
            dict_embed = {
                'description': f"❌ Vous ne pouvez pas mute un administrateur du serveur !\n\n*Justement...*\n*Cette tentative de mute va peux etre te causer beaucoup ennuis !!!*",
                'color': COLORS['red'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, ephemeral = True)
        else: 
            duree = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
            if duree >= timedelta(days = 28): 
                dict_embed = {
                    'description': f"❌ Vous ne pouvez pas mute une personne plus de 28 jours",
                    'color': COLORS['red'],
                }
                embed = discord.Embed.from_dict(dict_embed)
                await interaction.response.send_message(embed=embed, ephemeral = True)
            
            else:
                await member.timeout(duree, reason = reason)
                
                text_time = ''
                if days != 0: 
                    text_time += f' `{days}` jour(s),'
                if hours != 0: 
                    text_time += f' `{hours}` heure(s),'
                if minutes != 0: 
                    text_time += f' `{minutes}` minute(s),'
                if seconds != 0: 
                    text_time += f' `{seconds}` seconde(s),'
                text_time = text_time[:-1]
                
                dict_embed = {
                    'description': f"✅ {member.mention} a bien été mute. \n\n:white_small_square: **Temps:**{text_time} \n:white_small_square: **Raison:** `{reason}`",
                    'color': COLORS['green'],
                    'footer': {
                        'text': f'mute by {interaction.user.display_name}',
                        'icon_url': interaction.user.avatar.url
                    }
                }
                embed = discord.Embed.from_dict(dict_embed)
                await interaction.response.send_message(embed=embed)


async def setup(bot: DiscordBot):
    await bot.add_cog(Moderation(bot))
