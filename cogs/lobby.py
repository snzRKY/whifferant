import discord
from discord import app_commands
from discord.ext import commands
import typing
import sqlite3 as sql


def listToEmbedValue(list, guild):
    out = ""
    if (list == []):
        return "NuLL \n"
    for i in list:
        member = guild.get_member(int(i))
        out += member.name + "\n"
    return out


def lobbyEmbed(listA, listB, lobbyName, ownerIcon, guild):
    embed = discord.Embed()
    embed.set_author(name=lobbyName, icon_url=ownerIcon)
    embed.add_field(name="Attackers", value=listToEmbedValue(listA, guild), inline=True)
    embed.add_field(name="Defenders", value=listToEmbedValue(listB, guild), inline=True)
    return embed


db = sql.connect("./db/serverLobby.db")
cursor = db.cursor()


class nameOfCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # commandGoesHere
    async def lobbyAutoComplete(self, interaction: discord.Interaction, current: str) -> typing.List[
        app_commands.Choice[str]]:
        data = []
        items = []
        lobby = cursor.execute("SELECT * FROM lobby WHERE serverId = ?", (interaction.guild_id,))
        for l in lobby:
            items.append(l[1])
        for i in items:
            if (current.lower() in i.lower()):
                data.append(app_commands.Choice(name=i, value=i))
        return data

    @app_commands.command(name="lobby", description="Display Your Lobby")
    @app_commands.autocomplete(lobby=lobbyAutoComplete)
    async def lobby(self, interaction: discord.Interaction, lobby: str):
        selection = cursor.execute("SELECT * FROM lobby WHERE serverId = ? AND lobbyId = ?",
                                   (interaction.guild_id, lobby))
        for i in selection:
            attackerList = eval(i[2])
            defenderList = eval(i[3])
        await interaction.response.send_message(
            embed=lobbyEmbed(attackerList, defenderList, lobby, interaction.user.display_avatar,
                             interaction.user.guild))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(nameOfCommand(bot))