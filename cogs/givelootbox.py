import discord
from discord import app_commands
from discord.ext import commands
import typing
from tools import lootboxsystem
from tools import toolbox as tb


class givelootbox(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # commandGoesHere
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

    @app_commands.command(name="givelootbox", description="Give Member a Lootbox!")
    @app_commands.autocomplete(box=boxAutoComplete)
    @app_commands.describe(box="What would you like to give?", user="To Who would you like to give to?",
                           amount="How much?")
    @app_commands.checks.has_permissions(ban_members=True)
    async def givelootbox(self, interaction: discord.Interaction, box: str, user: str, amount: int):
        userId = user.lstrip("><@")
        userId = userId.rstrip("><@")
        if (lootboxsystem.giveLootBox(userId, interaction.guild_id, box, amount) == "None"):
            await interaction.response.send_message("That User Hasen't Signed Up yet")
        else:
            await interaction.response.send_message("Succesfully Gave Lootbox")
        return

    @givelootbox.error
    async def on_givelootbox_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(givelootbox(bot))