import discord
from discord import app_commands
from discord.ext import commands
import typing
import sqlite3 as sql
import json


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
    if (userList != None):
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
    else:
        return []

    return out


db = sql.connect("./db/serverLobby.db")
cursor = db.cursor()


class updatelobby(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

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

    # commandGoesHere
    @app_commands.command(name="updatelobby", description="What to do with your lobby?")
    @app_commands.autocomplete(lobby=lobbyAutoComplete, attackervc=vcAutoComplete, defendervc=vcAutoComplete)
    @app_commands.describe(
        lobby="Name of your lobby",
        action="What do you want to do?",
        attackers="Which attackers?",
        defenders="Which defenders?",
        attackervc="Which vc for attackers?",
        defendervc="Which vc for defenders?")
    @app_commands.choices(action=[
        discord.app_commands.Choice(name="Add", value=1),
        discord.app_commands.Choice(name="Delete", value=2),
        discord.app_commands.Choice(name="Switch Vc", value=3)])
    @app_commands.checks.has_permissions(move_members=True)
    async def updatelobby(self, interaction: discord.Interaction,
                          lobby: str, action: discord.app_commands.Choice[int],
                          attackers: typing.Optional[str],
                          defenders: typing.Optional[str],
                          attackervc: typing.Optional[str],
                          defendervc: typing.Optional[str]):
        guild = interaction.user.guild
        if (attackers != None):
            attackers = attackers.split()
            attackersList = userListToMemberList(attackers)
        else:
            attackersList = []
        if (defenders != None):
            defenders = defenders.split()
            defendersList = userListToMemberList(defenders)
        else:
            defendersList = []
        selection = cursor.execute("SELECT * FROM lobby WHERE serverId = ? AND lobbyId = ?",
                                   (interaction.guild_id, lobby))
        for i in selection:
            if (i):
                if (i[6] == 0):
                    attackerInLobby = eval(i[2])
                    defenderInLobby = eval(i[3])
                elif (i[6] == 1):
                    await interaction.response.send_message("Lobby Already In Session /end to end session!")
                    return
        if (action.name == "Add"):
            for a in attackersList:
                if (a not in attackerInLobby):
                    attackerInLobby.append(a)
            for d in defendersList:
                if (d not in defenderInLobby):
                    defenderInLobby.append(d)
            # append attackers and defenders to the lobby then update lobby in data base
            if ((len(attackerInLobby) > 5) or (len(defenderInLobby) > 5)):
                await interaction.response.send_message("Update Exceeds Maximum Of 5 People Per Team!")
                return
            cursor.execute("UPDATE lobby SET attackers = ? WHERE serverId =? AND lobbyId =?",
                           (str(attackerInLobby), interaction.guild_id, lobby))
            cursor.execute("UPDATE lobby SET defenders = ? WHERE serverId =? AND lobbyId =?",
                           (str(defenderInLobby), interaction.guild_id, lobby))
            db.commit()
            await interaction.response.send_message(
                embed=lobbyEmbed(attackerInLobby, defenderInLobby, lobby, interaction.user.display_avatar,
                                 interaction.user.guild))
            return
        elif (action.name == "Delete"):
            for a in attackersList:
                if (a in attackerInLobby):
                    attackerInLobby.remove(a)
            for d in defendersList:
                if (d in defenderInLobby):
                    defenderInLobby.remove(d)
            cursor.execute("UPDATE lobby SET attackers = ? WHERE serverId =? AND lobbyId =?",
                           (str(attackerInLobby), interaction.guild_id, lobby))
            cursor.execute("UPDATE lobby SET defenders = ? WHERE serverId =? AND lobbyId =?",
                           (str(defenderInLobby), interaction.guild_id, lobby))
            db.commit()
            await interaction.response.send_message(
                embed=lobbyEmbed(attackerInLobby, defenderInLobby, lobby, interaction.user.display_avatar,
                                 interaction.user.guild))
            return
        elif (action.name == "Switch Vc"):
            if (attackervc != None):
                attackerVcId = discord.utils.get(interaction.user.guild.channels, name=attackervc).id
                cursor.execute("UPDATE lobby SET attackerVc = ? WHERE serverId = ? AND lobbyID = ?",
                               (attackerVcId, interaction.guild_id, lobby))
            if (defendervc != None):
                defenderVcId = discord.utils.get(interaction.user.guild.channels, name=defendervc).id
                cursor.execute("UPDATE lobby SET defenderVc = ? WHERE serverId = ? AND lobbyID = ?",
                               (defenderVcId, interaction.guild_id, lobby))
            if (attackervc == None) and (defendervc == None):
                await interaction.response.send_message("You never gave me the vc's you wanted to switch to...")
                return
            db.commit()
            await interaction.response.send_message("Successfully updated your lobby vc!")
            return

    @updatelobby.error
    async def on_updatelobby_error(self, interaction: discord.Interaction,
                                   error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(updatelobby(bot))