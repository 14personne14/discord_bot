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
            categories_options = []
            channels_options = {}
            
            for category, channels in hierarchy:
                at_least_one_text_channel = False
                
                # Add channels in dict
                for channel in channels:
                    if isinstance(channel, discord.TextChannel):
                        at_least_one_text_channel = True
                        if str(category.id) in channels_options:
                            channels_options[str(category.id)].append(discord.SelectOption(label = channel.name, description = f"id:{channel.id}", value=str(channel.id)))
                        else:
                            channels_options[str(category.id)] = [ discord.SelectOption(label = channel.name, description = f"id:{channel.id}", value=str(channel.id)) ]
                
                # Add categories in list
                if at_least_one_text_channel:
                    categories_options.append(discord.SelectOption(label = category.name, description = f"id:{category.id}", value=str(category.id)))
            
            user_id = interaction.user.id
            view = ViewTextChannel(categories_options, channels_options, user_id)
            dict_embed = {
                'description': '🔷 Vous pouvez choisir ci-dessous une **catégorie** de salon.',
                'color': COLORS['blue'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, view=view)
            await view.wait()
            
            # Timeout
            if view.channel == None:
                dict_embed = {
                    'description': f"❌ Le temps d'attente est dépassé.",
                    'color': COLORS['red'],
                }
                embed = discord.Embed.from_dict(dict_embed)
                await interaction.edit_original_response(embed=embed, view=None)
            # Update new role channel
            else:
                self.bot.database.insert_or_update(f"INSERT INTO Guilds (id, id_channel_role) VALUES ({interaction.guild.id}, {view.channel}) ON DUPLICATE KEY UPDATE id_channel_role = {view.channel}")
                
                new_channel = self.bot.get_channel(int(view.channel))
                
                self.bot.log(
                    message=f"New role channel for guild '{interaction.guild.name}' : '{new_channel.name}'",
                    name="discord.setup.channel_role"
                )
                
                dict_embed = {
                    'description': f"✅ Le nouveau salon pour les roles est maintenant {new_channel.mention}",
                    'color': COLORS['green'],
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
