import discord


async def followup_embed(data: dict, interaction: discord.Interaction, *, ephemeral: bool = False):
    embed = discord.Embed.from_dict(data)
    await interaction.followup.send(embed=embed, ephemeral=ephemeral)

async def send_embed(data: dict, interaction: discord.Interaction, *, ephemeral: bool = False):
    embed = discord.Embed.from_dict(data)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
