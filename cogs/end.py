import discord
from discord import app_commands
from discord.ext import commands
import sqlite3 as sql
import typing
from tools import lootboxsystem
from tools import toolbox as tb

#Table Format
#table name: lobby
#table values: serverId,lobbyId,attackers,defenders
#serverId integer
#lobbyId string
#attackers string'd list eval([id1,id2,id3,id4,id5])
#defenders string's list eval([id6,id7,id8,id9,id10])
#attackerVc int
#defenderVc int
#status 0 or 1
db = sql.connect("./db/serverLobby.db")
cursor = db.cursor()

class end(commands.Cog):
  def __init__(self,bot: commands.Bot) -> None:
    self.bot = bot
  async def lobbyAutoComplete(self,interaction: discord.Interaction,current: str) ->         typing.List[app_commands.Choice[str]]:
    data = []
    items = []
    lobby = cursor.execute("SELECT * FROM lobby WHERE serverId = ?",(interaction.guild_id,))
    for l in lobby:
      items.append(l[1])
    for i in items:
      if (current.lower() in i.lower()):
        data.append(app_commands.Choice(name=i, value=i))
    return data
  #commandGoesHere
  @app_commands.command(name ="end", description ="End you lobby [Still Working On This Feature]")
  @app_commands.autocomplete(lobby = lobbyAutoComplete)
  @app_commands.describe(lobby = "Lobby Name",action="Save or Delete This Lobby",winner = "Which Team Won?")
  @app_commands.choices(action = [
    discord.app_commands.Choice(name="save",value = 1),
    discord.app_commands.Choice(name="delete",value=2)],
    winner = [discord.app_commands.Choice(name="Attackers",value = 1),
    discord.app_commands.Choice(name ="Defenders",value = 2),
    discord.app_commands.Choice(name = "None",value = 3)])
  @app_commands.checks.has_permissions(move_members=True)
  async def end(self,interaction:discord.Interaction,lobby:str,action: discord.app_commands.Choice[int],winner: discord.app_commands.Choice[int],):
    selection = cursor.execute("SELECT * FROM lobby WHERE serverId = ? AND lobbyId = ?",(interaction.guild_id,lobby))
    for i in selection:
      if(i[6] == 0):
        await interaction.response.send_message("This lobby does not appear to be in session do /start")
      elif(i[6] == 1):
        cursor.execute("UPDATE lobby SET status = 0 WHERE serverId = ? AND lobbyId = ?",(interaction.guild_id,lobby))
        db.commit()
        failed=[]
        attackerList = eval(i[2])
        defenderList = eval(i[3])
        if(winner.name == "Attackers"):
          for a in attackerList:
            if(lootboxsystem.giveLootBox(a,interaction.guild_id,"Denz Tenz",1) == "None"):
              failed.append(a)
          for d in defenderList:
            if(lootboxsystem.giveCredits(d,interaction.guild_id,5)=="None"):
              failed.append(d)
        elif(winner.name == "Defenders"):
          for d in defenderList:
            if(lootboxsystem.giveLootBox(d,interaction.guild_id,"Denz Tenz",1) == "None"):
              failed.append(d)
          for a in attackerList:
            if(lootboxsystem.giveCredits(a,interaction.guild_id,5) == "None"):
              failed.append(a)
        elif(winner.name == "None"):
          pass
        if(action.name == "save"):
          guild = interaction.user.guild
          lobbyVcId = i[7]
          if(attackerList):
            for a in attackerList:
              member = guild.get_member(int(a))
              channel = guild.get_channel(lobbyVcId)
              await member.move_to(channel)
          if(defenderList):
            for d in defenderList:
              member = guild.get_member(int(d))
              channel = guild.get_channel(lobbyVcId)
              await member.move_to(channel)
          await interaction.response.send_message("Saved Lobby's Session and Ended")
          if(len(failed) > 0):
            await interaction.followup.send("Failed to reward " + len(failed) + " member(s) please make sure everyone has used /signup")
        elif(action.name == "delete"):
          guild = interaction.user.guild
          lobbyVcId = i[7]
          if(attackerList):
            for a in attackerList:
              member = guild.get_member(int(a))
              channel = guild.get_channel(lobbyVcId)
              await member.move_to(channel)
          if(defenderList):
            for d in defenderList:
              member = guild.get_member(int(d))
              channel = guild.get_channel(lobbyVcId)
              await member.move_to(channel)
          cursor.execute("DELETE FROM lobby WHERE serverId = ? AND lobbyId = ?",(interaction.guild_id,lobby))
          db.commit()
          await interaction.response.send_message("Successfully ended and deleted the lobby!")
          if(len(failed) > 0):
            await interaction.followup.send("Failed to reward " + len(failed) + " member(s) please make sure everyone has used /signup")
          return
  @end.error
  async def on_end_error(self,interaction: discord.Interaction,
                               error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
      await interaction.response.send_message(str(error), ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(end(bot))