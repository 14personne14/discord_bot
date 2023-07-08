import discord
from discord.ui import Modal, TextInput, Select
from typing import Literal

class TuPrefere(Modal, title='Création Tu prefere'):
    choix_1 = TextInput(label='Choix 1', style=discord.TextStyle.short, required=True, placeholder='Avion', min_length=2)
    choix_2 = TextInput(label='Choix 2', style=discord.TextStyle.short, required=True, placeholder='Train', min_length=2)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Votre réponse a bien été enregistrée !', ephemeral=True)
        self.stop()

class ChannelRole(Modal, title='Définir Salon Role'):
    id_channel = TextInput(label='Identifiant du salon', style=discord.TextStyle.short, required=True, placeholder='XxxxxXxxxxXxxxxXxx', min_length=18, max_length=19)
    test = Select(placeholder="un_test", options=[
        discord.SelectOption(label="lab1", value="test1"),
        discord.SelectOption(label="lab2", value="test2"),
        discord.SelectOption(label="lab3", value="test3")
    ], min_values=1, max_values=1)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.interaction = interaction
        self.stop()
    