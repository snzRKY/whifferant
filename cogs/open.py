import discord
from discord import app_commands
from discord.ext import commands
from tools import lootboxsystem
from tools import toolbox as tb
import typing
import math


class open(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def boxAutoComplete(self, interaction: discord.Interaction, current: str) -> typing.List[
        app_commands.Choice[str]]:
        data = []
        items = []
        for c in tb.listOutCsv("boxes.csv"):
            items.append(c)
        for i in items:
            if (current.lower() in i.lower()):
                data.append(app_commands.Choice(name=i, value=i))
        return data

    # commandGoesHere
    @app_commands.command(name="open", description="Opens a Lootbox")
    @app_commands.autocomplete(box=boxAutoComplete)
    @app_commands.describe(box="Which box would you like to open", amount="How many Of them?")
    async def openlootbox(self, interaction: discord.Interaction, box: str, amount: int):
        aboveStr = ""
        if (amount > 9):
            response = lootboxsystem.openLootBox(interaction.user.id, interaction.guild_id, box, 9)
            aboveStr = "Open'd 9 Lootboxes (Max 9)"
        else:
            response = lootboxsystem.openLootBox(interaction.user.id, interaction.guild_id, box, amount)
        if (response == "You have 0 Boxes Left"):
            await interaction.response.send_message("You don't have that box!")
        elif (response == "Inefficient Amount"):
            await interaction.response.send_message("You don't have that many lootboxes!")
        elif (response == "You don't own this Lootbox"):
            await interaction.response.send_message("You don't own this Lootbox")
        elif (response == "User /signup to access This Command!"):
            await interaction.response.send_message("User /signup to access This Command!")
        else:
            embed = discord.Embed(title="You got: ")
            for i in response:
                emoji = tb.emojiFinder(i)
                embed.add_field(name=emoji + " " + i, value="1x")
            if (aboveStr != ""):
                await interaction.response.send_message(aboveStr, embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(open(bot))