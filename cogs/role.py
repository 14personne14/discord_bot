# Discord
import discord
from discord.ext import commands
from discord import app_commands

# My import 
from classes.utils import COLORS
from classes.discordbot import DiscordBot
from classes.embed import send_embed
from views.persistence import PersistentView
from views.modal import ChannelRole
from views.select import ViewTextChannel


class Role(commands.Cog, name="Role"):
    def __init__(self, bot: DiscordBot):
        self.bot = bot
    
    @app_commands.command(name="setup", description="Setup un element du serveur")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Salon roles", value="channel_role")
    ])
    @app_commands.guild_only()
    async def setup(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        if choices.value == "channel_role":
            hierarchy = interaction.guild.by_category()
            select_options = []
            second_select_options = {}
            for category, channels in hierarchy:
                good_text_channel = False
                for channel in channels:
                    if isinstance(channel, discord.TextChannel):
                        good_text_channel = True
                        if str(category.id) in second_select_options:
                            second_select_options[str(category.id)].append(discord.SelectOption(label = channel.name, description = f"id:{channel.id}", value=channel.id))
                        else:
                            second_select_options[str(category.id)] = [ discord.SelectOption(label = channel.name, description = f"id:{channel.id}", value=channel.id) ]
                if good_text_channel:
                    select_options.append(discord.SelectOption(label = category.name, description = f"id:{category.id}", value=category.id))
            
            select = ViewTextChannel(select_options, second_select_options)
            dict_embed = {
                'description': '🔷 Vous pouvez choisir ci-dessous une catégorie de salon.',
                'color': COLORS['blue'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, view=select)
            await select.wait()
            
            if select.channel != None:
                req = self.bot.database.select(f"SELECT * FROM Guilds WHERE id={interaction.guild.id};")
                if len(req) == 0:
                    self.bot.database.insert(f"INSERT INTO Guilds (id, id_channel_role) VALUES ({interaction.guild.id}, {select.channel});")
                else:
                    self.bot.database.update(f"UPDATE Guilds SET id_channel_role = {select.channel} WHERE id = {interaction.guild.id};")
                
                dict_embed = {
                    'description': f"✅ Le nouveau salon pour les roles est maintenant {self.bot.get_channel(int(select.channel)).mention}",
                    'color': COLORS['green'],
                }
                embed = discord.Embed.from_dict(dict_embed)
                await interaction.edit_original_response(embed=embed, view=None)
            else:
                dict_embed = {
                    'description': f"❌ Le temps d'attente est dépassé.",
                    'color': COLORS['red'],
                }
                embed = discord.Embed.from_dict(dict_embed)
                await interaction.edit_original_response(embed=embed, view=None)
        
        else:
            await send_embed(
                {'description': f"❌ Le choix est incorrect. Veuillez réessayer.", 'color': COLORS['red']}, 
                interaction, 
                ephemeral=True
            )
    
    @app_commands.command(name="persistance", description="Créé une vue persistante.")
    async def persistance(self, interaction: discord.Interaction):
        await interaction.response.send_message('Bonjour !', view=PersistentView())

async def setup(bot: DiscordBot):
    await bot.add_cog(Role(bot))
