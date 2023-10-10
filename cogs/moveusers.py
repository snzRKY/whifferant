import discord
from discord import app_commands
from discord.ext import commands
import sqlite3 as sql


class moveusers(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # commandGoesHere
    @app_commands.command(name="moveusers", description="Move the users in your voice channel!")
    @app_commands.describe(attackers="Mention All Attackers", defenders="Mention all Defenders")
    @app_commands.checks.has_permissions(move_members=True)
    async def moveusers(self, interaction: discord.Interaction, attackers: str, defenders: str):
        await interaction.response.send_message("Proccessing Information...")

        def check(m):
            return m.author.id == interaction.user.id

        vcDataBase = sql.connect("./db/vcsaves.db")
        vcCursor = vcDataBase.cursor()
        vcCursor.execute(
            "CREATE TABLE IF NOT EXISTS vc(serverID integer ,attackvcID integer ,defendvcID integer)"
        )
        serverSelection = list(
            vcCursor.execute("SELECT * FROM vc WHERE serverID = ?",
                             (interaction.guild_id,)))
        if (serverSelection != []):
            attackvc = int(serverSelection[0][1])
            defendvc = int(serverSelection[0][2])
        else:
            await interaction.edit_original_response("Use /savevc first!")
            return
        attackvc = int(attackvc)
        defendvc = int(defendvc)
        attackers = attackers.split()
        defenders = defenders.split()
        guild = interaction.user.guild
        print(guild)
        valUserDB = sql.connect("./db/valorantuser.db")
        valUserCursor = valUserDB.cursor()
        userNames = list(valUserCursor.execute("SELECT * FROM valuser"))
        for a in attackers:
            if (a != None):
                if (a.isalpha() == False):
                    a = a.lstrip("><@")
                    a = a.rstrip("><@")
                    member = guild.get_member(int(a))
                    channel = guild.get_channel(attackvc)
                    await member.move_to(channel)
                else:
                    for mem in userNames:
                        if (a.lower() == mem[1].lower()):
                            member = guild.get_member(int(mem[0]))
                            channel = guild.get_channel(attackvc)
                            await member.move_to(channel)
        for d in defenders:
            if (d != None):
                if (d.isalpha() == False):
                    d = d.lstrip("><@")
                    d = d.rstrip("><@")
                    member = guild.get_member(int(d))
                    channel = guild.get_channel(defendvc)
                    await member.move_to(channel)
                else:
                    for mem in userNames:
                        if (d.lower() == mem[1].lower()):
                            member = guild.get_member(int(mem[0]))
                            channel = guild.get_channel(defendvc)
                            await member.move_to(channel)
        await interaction.edit_original_response("Succefully Reallocated Users")
        return

    @moveusers.error
    async def on_moveusers_error(self, interaction: discord.Interaction,
                                 error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(moveusers(bot))