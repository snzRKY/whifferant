import discord
from discord import app_commands
from discord.ext import commands

from cogs import rmap

def editedMapSpin(removedMaps,mapPool):
    for i in (removedMaps):
      i = i.lower()
      for y in range(len(mapPool)):
        mapPool[y] = mapPool[y].lower()
      if(i in mapPool):
        mapPool.remove(i)
    return rmap.mapChooser(mapPool)

class editedrmap(commands.Cog):
  def __init__(self,bot: commands.Bot) -> None:
    self.bot = bot

  #commandGoesHere
  @app_commands.command(name="rmapedit", description="Random Edited Map Generator")
  @app_commands.describe(remove="list maps to remove from the map pool")
  async def editedrmap(self,interaction: discord.Interaction, remove: str):
    maps = [
      'Bind', 'Haven', 'Breeze', 'Icebox', 'Split', 'Ascent', 'Fracture', 'Pearl'
    ]
    remove = remove.split()
    mapName, image, embedColor = editedMapSpin(remove, maps)
    embed = discord.Embed(title=mapName, color=embedColor)
    embed.set_image(url=image)
    await interaction.response.send_message(embed=embed)
    return


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(editedrmap(bot))