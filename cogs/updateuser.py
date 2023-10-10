import discord
from discord import app_commands
from discord.ext import commands
import sqlite3 as sql

def update(userId,valuser):
  def check(m):
    if ("#" in m):
      m = m.split("#")
      return m[0]
    else:
      return True
  if (check(valuser) == True):
    valuser = valuser
  else:
    valuser = check(valuser)
  db = sql.connect("./db/valorantuser.db")
  cursor = db.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS valuser(discordID integer,valUser text)")
  selection = list(cursor.execute("SELECT * FROM valuser"))
  if(selection != []):
    for users in selection:
      if (users[0] == userId):
        cursor.execute("UPDATE valuser SET valUser = ? WHERE discordID = ?",(valuser, userId))
        db.commit()
        return("Successfully Updated Your Valorant Username!")
        db.commit()
  else:
    return ("You need to sign up first! /signup")
  return

class updateuser(commands.Cog):
  def __init__(self,bot: commands.Bot) -> None:
    self.bot = bot

  #commandGoesHere
  @app_commands.command(name="updateuser",description="Updates The Val Username Conencted To Your Discord")
  @app_commands.describe(valuser="Your Valorant Username")
  async def updateuser(self,interaction: discord.Interaction, valuser: str):
    await interaction.response.send_message(update(interaction.user.id,valuser))


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(updateuser(bot))