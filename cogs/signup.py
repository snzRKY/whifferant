import discord
from discord import app_commands
from discord.ext import commands
import sqlite3 as sql
from tools import lootboxsystem

def sign(userId,serverId,valuser):
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
  cursor.execute(
    "CREATE TABLE IF NOT EXISTS valuser(discordID integer,valUser text)")
  if (lootboxsystem.signUp(userId,serverId) == "User Already Completed A Signup"):
    return ("User Already Completed A Signup (If You are trying to update your Connected Valorant Username use /updateuser")
  else:
    selection = list(cursor.execute("SELECT * FROM valuser"))
    for users in selection:
      if (users[0] == userId):
        return ("Successfully Completed Signup")
    cursor.execute("INSERT OR IGNORE INTO valuser(discordID, valUser) VALUES (?,?)",(userId, valuser))
    db.commit()
    return ("Successfully Completed Signup")
  return

class signup(commands.Cog):
  def __init__(self,bot: commands.Bot) -> None:
    self.bot = bot

  #commandGoesHere
  @app_commands.command(name="signup",
                  description="Connects Your Discord To A Valorant Username")
  @app_commands.describe(valuser="Your Valorant Username")
  async def signup(self,interaction: discord.Interaction, valuser: str):
    await interaction.response.send_message(sign(interaction.user.id,interaction.guild_id,valuser))


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(signup(bot))