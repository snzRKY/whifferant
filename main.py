import discord
from discord.ext import commands
from discord import app_commands
import os

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=discord.Intents.all())

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
        await bot.tree.sync()

    async def on_ready(self):
        print('Connected')


bot = MyBot()


@bot.on_error
async def on_bot_error():
    return


@bot.tree.command(name="ping", description="Current Ping Of Bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f'**Pong!** Latency: {round(bot.latency * 1000)}ms', ephemeral=True)
    print(f'**Pong!** Latency: {round(bot.latency * 1000)}ms')
    return


try:
    bot.run("Token Here")
except discord.errors.HTTPException:
    print("\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("kill 1")
    os.system("python ./tools/restarter.py")