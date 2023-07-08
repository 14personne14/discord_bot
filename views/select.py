# Discord
import discord
from discord.ui import View, Select, Button

# My import
from classes.utils import COLORS

class SelectTextChannel(Select):
    def __init__(self):
        self.choix = None 
        options = [
            discord.SelectOption(
                label = "hgdfhjsgf",
                description = "Le salon 1"
            ), 
            discord.SelectOption(
                label = "Salon 2",
                description = "Le salon 2"
            )
        ]
        super().__init__(options = options, placeholder = "Choisir un salon", min_values = 1, max_values = 1)

class ViewTextChannel(View):
    def __init__(self, options, second_options):
        super().__init__(timeout=60)
        
        self.options = options
        self.second_options = second_options
        self.channel = None
        
        select = Select(
            options = self.options,
            placeholder = "Choisissez une catégorie",
            custom_id = "select_categories",
            min_values = 1,
            max_values = 1
        )
        self.add_item(select)
    
    async def interaction_check(self, interaction: discord.Interaction):
        if self.children[0].custom_id == "select_categories":
            category_id = self.children[0].values[0]
            self.clear_items()
            new_select = Select(
                options = self.second_options[category_id],
                placeholder = "Choisissez un salon",
                custom_id = "select_channel",
                min_values = 1,
                max_values = 1
            )
            self.add_item(new_select)
            button = Button(label="Revenir", emoji = "◀️", style=discord.ButtonStyle.grey)
            self.add_item(button)
            dict_embed = {
                'description': '🔷 Vous pouvez maintenant choisir le **nouveau salon textuel**.',
                'color': COLORS['blue'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.edit_message(embed=embed, view=self)
        elif self.children[0].custom_id == "select_channel" and self.children[0].values != []:
            self.channel = self.children[0].values[0]
            self.children[0].disabled = True
            await interaction.response.edit_message(view=self)
            self.stop()
        else:
            self.clear_items()
            select = Select(
                options = self.options,
                placeholder = "Choisissez une catégorie",
                custom_id = "select_categories",
                min_values = 1,
                max_values = 1
            )
            self.add_item(select)
            dict_embed = {
                'description': '🔷 Vous pouvez choisir ci-dessous une catégorie de salon.',
                'color': COLORS['blue'],
            }
            embed = discord.Embed.from_dict(dict_embed)
            await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        self.stop()
