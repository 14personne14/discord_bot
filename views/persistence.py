import discord
from discord.ui import View, Button

class PersistentView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Green', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message('C\' vert !')
    
    @discord.ui.button(label='Red', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message('C\' rouge !')
        
    @discord.ui.button(label='Gray', style=discord.ButtonStyle.gray, custom_id='persistent_view:gray')
    async def gray(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message('C\' gris !')
