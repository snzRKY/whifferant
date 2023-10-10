import discord
from discord import app_commands
from discord.ext import commands
import typing
import sqlite3 as sql


def vcsaver(attackvcID, defendvcID, serverID):
    vcDataBase = sql.connect("./db/vcsaves.db")
    cursor = vcDataBase.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS vc(serverID integer ,attackvcID integer ,defendvcID integer)"
    )
    select = list(cursor.execute("SELECT * FROM vc"))
    for servers in select:
        if (servers[0] == serverID):
            cursor.execute(
                "UPDATE vc SET attackvcID = ?,defendvcID = ? WHERE serverID = ?",
                (attackvcID, defendvcID, serverID))
            vcDataBase.commit()
            return ("Successfully Updated VC's!")
    cursor.execute("INSERT INTO vc(serverID,attackvcID,defendvcID) VALUES (?,?,?)", (serverID, attackvcID, defendvcID))
    vcDataBase.commit()
    return ("Successfully Saved VC's!")


class savevc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # commandGoesHere
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

    @app_commands.command(name="savevc", description="Save attacker's & defender's vcs")
    @app_commands.autocomplete(attackervc=vcAutoComplete, defendervc=vcAutoComplete)
    @app_commands.describe(attackervc="What do you want your Attacker's Vc To be?",
                           defendervc="What do you want your Defender's Vc To be?")
    @app_commands.checks.has_permissions(move_members=True)
    async def savevc(self, interaction: discord.Interaction, attackervc: str, defendervc: str):
        guild = interaction.user.guild
        serverID = interaction.guild_id
        attackvcID = discord.utils.get(guild.channels, name=attackervc).id
        defendvcID = discord.utils.get(guild.channels, name=defendervc).id
        await interaction.response.send_message(vcsaver(attackvcID, defendvcID, serverID))

    @savevc.error
    async def on_savevc_error(self, interaction: discord.Interaction,
                              error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(savevc(bot))