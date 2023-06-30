import discord
from discord.ui import Modal, TextInput

class ModalTuPrefere(Modal, title='Tu prefere'):
    choix_1 = TextInput(label='Choix 1', style=discord.TextStyle.short, required=True, placeholder='Avion', min_length=2)
    choix_2 = TextInput(label='Choix 2', style=discord.TextStyle.short, required=True, placeholder='Train', min_length=2)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Votre réponse a bien été enregistrée !', ephemeral=True)
        self.stop()
