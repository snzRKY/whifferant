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

class start(commands.Cog):
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

    # commandGoesHere
    @app_commands.command(name="start", description="Start a Lobby!")
    @app_commands.autocomplete(lobby=lobbyAutoComplete)
    @app_commands.checks.has_permissions(move_members=True)
    async def start(self, interaction: discord.Interaction, lobby: str):
        selection = cursor.execute("SELECT * FROM lobby WHERE serverId = ? AND lobbyId = ?",
                                   (interaction.guild_id, lobby))
        for i in selection:
            if (i[6] == 1):
                await interaction.response.send_message("Lobby is already in session /end to end session")
            elif (i[6] == 0):
                attackerList = eval(i[2])
                defenderList = eval(i[3])
                attackerVcId = i[4]
                defenderVcId = i[5]
                guild = interaction.user.guild
                for a in attackerList:
                    member = guild.get_member(int(a))
                    channel = guild.get_channel(attackerVcId)
                    await member.move_to(channel)
                for d in defenderList:
                    member = guild.get_member(int(d))
                    channel = guild.get_channel(defenderVcId)
                    await member.move_to(channel)

                cursor.execute("UPDATE lobby SET status = 1 WHERE serverId = ? AND lobbyId = ?",
                               (interaction.guild_id, lobby))
                db.commit()
                await interaction.response.send_message(str(lobby) + " has offically started /end to end this session")
                return

    @start.error
    async def on_start_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("Someone in the lobby is not in a voice channel!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(start(bot))