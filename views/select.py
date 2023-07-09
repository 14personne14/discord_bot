# Discord
import discord
from discord.ui import View, Select, Button

# My import
from classes.utils import COLORS


class SelectCategory(Select):
    def __init__(self, view):
        self.parent_view = view
        super().__init__(options = self.parent_view.categories_options, placeholder = "Choisissez une catégorie", custom_id = "select_categories", min_values = 1, max_values = 1)

    async def callback(self, interaction: discord.Interaction):
        if self.parent_view.user_id == interaction.user.id:
            category_id = self.values[0]
            for i in range(len(self.options)):
                self.options[i].default = False
            
            for i in range(len(self.options)):
                if self.options[i].value == category_id:
                    self.options[i].default = True
            await self.parent_view.to_second_choice(interaction, category_id)
        else: 
            dict_embed = {
                'description': f"❌ Tu ne peux pas interagir avec ce message !",
                'color': COLORS['red'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, ephemeral=True)


class SelectChannel(Select):
    def __init__(self, view, category_id):
        self.parent_view = view
        super().__init__(options = self.parent_view.channels_options[category_id], placeholder = "Choisissez un salon", custom_id = "select_channel", min_values = 1, max_values = 1)

    async def callback(self, interaction: discord.Interaction):
        if self.parent_view.user_id == interaction.user.id:
            self.parent_view.channel = self.values[0]
            self.parent_view.stop()
        else: 
            dict_embed = {
                'description': f"❌ Tu ne peux pas interagir avec ce message !",
                'color': COLORS['red'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class ViewTextChannel(View):
    def __init__(self, categories_options, channels_options, user_id):
        super().__init__(timeout=60)
        
        self.categories_options = categories_options
        self.channels_options = channels_options
        self.channel = None
        self.user_id = user_id
        
        self.select_category = SelectCategory(self)
        self.select_channel = None
        self.add_item(self.select_category)
    
    async def to_second_choice(self, interaction: discord.Interaction, category_id,):
        # Update SelectCategory
        self.remove_item(self.select_category)
        self.add_item(self.select_category)
        
        # Add or update SelectChannel
        if self.select_channel == None:
            self.select_channel = SelectChannel(self, category_id)
            self.add_item(self.select_channel)
            
            dict_embed = {
                'description': '🔷 Vous pouvez maintenant choisir le nouveau **salon textuel**.',
                'color': COLORS['blue'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.edit_message(embed=embed, view=self)
        else: 
            self.remove_item(self.select_channel)
            self.select_channel = SelectChannel(self, category_id)
            self.add_item(self.select_channel)
            await interaction.response.edit_message(view=self)
    
    async def on_timeout(self):
        self.stop()
