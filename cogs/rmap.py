import discord
from discord import app_commands
from discord.ext import commands
import random

title = ""
image = ""
color = ""


def mapChooser(mapPool):
    select = (random.choice(mapPool)).capitalize()

    if (select == 'Bind'):
        title = "Bind"
        image = "https://cdn.discordapp.com/attachments/1019845027398160404/1046941391420395671/unknown.png"
        color = 0xc27c0e

    if (select == 'Haven'):
        title = "Haven"
        image = "https://cdn.discordapp.com/attachments/1019845027398160404/1046941483623780393/unknown.png"
        color = 0x992d22

    if (select == 'Breeze'):
        title = "Breeze"
        image = "https://media.discordapp.net/attachments/1019845027398160404/1046941709856165919/unknown.png?width=720&height=405"
        color = 0x1abc9c

    if (select == 'Icebox'):
        title = "Icebox"
        image = "https://cdn.discordapp.com/attachments/1019845027398160404/1046941914936643675/unknown.png"
        color = 0x3498db

    if (select == 'Split'):
        title = "Split"
        image = "https://cdn.discordapp.com/attachments/1019845027398160404/1046942019802648586/unknown.png"
        color = 0x607d8b

    if (select == 'Ascent'):
        title = "Ascent"
        image = "https://cdn.discordapp.com/attachments/1019845027398160404/1046942117672525974/unknown.png"
        color = 0xe74c3c

    if (select == 'Fracture'):
        title = "Fracture"
        image = "https://cdn.discordapp.com/attachments/1019845027398160404/1046942298010820628/unknown.png"
        color = 0x9BD0B4

    if (select == 'Pearl'):
        title = "Pearl"
        image = "https://cdn.discordapp.com/attachments/1019845027398160404/1046942389681541211/unknown.png"
        color = 0x3498db
    return title, image, color


class Rmap(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="rmap", description="Random Map Generator")
    async def rmap(self, interaction: discord.Interaction):
        maps = ['Bind', 'Haven', 'Breeze', 'Icebox', 'Split', 'Ascent', 'Fracture', 'Pearl']
        mapName, image, embedColor = mapChooser(maps)
        embed = discord.Embed(title=mapName, color=embedColor)
        embed.set_image(url=image)
        await interaction.response.send_message(embed=embed)
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Rmap(bot))