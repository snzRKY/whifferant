import discord
from discord import app_commands
from discord.ext import commands
import sqlite3 as sql
import typing

db = sql.connect("./db/serverLobby.db")
cursor = db.cursor()


# Table Format
# table name: lobby
# table values: serverId,lobbyId,attackers,defenders
# serverId integer
# lobbyId string
# attackers string'd list eval([id1,id2,id3,id4,id5])
# defenders string's list eval([id6,id7,id8,id9,id10])
# attackerVc int
# defenderVc int
# status 0 or 1
# lobbyVc int

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


def userListToMemberList(userList):
    valUserDB = sql.connect("./db/valorantuser.db")
    valUserCursor = valUserDB.cursor()
    userNames = list(valUserCursor.execute("SELECT * FROM valuser"))
    out = []
    for i in userList:
        if (i != None):
            if (i.isalpha() == False):
                i = i.lstrip("><@")
                i = i.rstrip("><@")
                out.append(i)
            else:
                for mem in userNames:
                    if (i.lower() == mem[1].lower()):
                        out.append(mem[0])
    return out


class createlobby(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def vcAutoComplete(self, interaction: discord.Interaction, current: str) -> typing.List[
        app_commands.Choice[str]]:
        data = []
        channels = []
        for c in interaction.user.guild.voice_channels:
            channels.append(c)
        for chan in channels:
            if (current.lower() in chan.name.lower()):
                data.append(app_commands.Choice(name=chan.name, value=chan.name))
        return data

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS lobby(serverId integer,lobbyId string,attackers string,defenders string,attackerVc integer, defenderVc integer,status boolean,lobbyVc integer)")

    @app_commands.command(name="createlobby", description="Create a Lobby")
    @app_commands.autocomplete(attackervc=vcAutoComplete, defendervc=vcAutoComplete, lobbyvc=vcAutoComplete)
    @app_commands.describe(name="What would you like to call your lobby?",
                           attackers="Who are the attackers?",
                           defenders="Who are the defenders?",
                           attackervc="Where should we set the attacker vc?",
                           defendervc="Where should we set the defender vc?",
                           lobbyvc="Where should we set the lobby vc?")
    @app_commands.checks.has_permissions(move_members=True)
    async def createlobby(self, interaction: discord.Interaction, name: str, attackers: str, defenders: str,
                          attackervc: str, defendervc: str, lobbyvc: str):
        attackers = attackers.split()
        defenders = defenders.split()
        if ((len(attackers) > 5) or (len(defenders) > 5)):
            await interaction.response.send_message("Error: Tried Adding more than 5 people to lobby")
            return
        attackerList = userListToMemberList(attackers)
        defenderList = userListToMemberList(defenders)
        selection = cursor.execute("SELECT * FROM lobby WHERE serverId = ? AND lobbyId = ?",
                                   (interaction.guild_id, name,))
        for lobbies in selection:
            if (lobbies):
                await interaction.response.send_message("Lobby with that name already exist!")
                return

        attackerVcId = discord.utils.get(interaction.user.guild.channels, name=attackervc).id
        defenderVcId = discord.utils.get(interaction.user.guild.channels, name=defendervc).id
        lobbyVcId = discord.utils.get(interaction.user.guild.channels, name=lobbyvc).id
        cursor.execute("INSERT OR IGNORE INTO lobby VALUES (?,?,?,?,?,?,?,?)", (
        interaction.guild_id, name, str(attackerList), str(defenderList), attackerVcId, defenderVcId, 0, lobbyVcId))
        db.commit()
        await interaction.response.send_message(
            embed=lobbyEmbed(attackerList, defenderList, name, interaction.user.display_avatar, interaction.user.guild))

    @createlobby.error
    async def on_createlobby_error(self, interaction: discord.Interaction,
                                   error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(createlobby(bot))