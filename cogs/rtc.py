import discord
from discord import app_commands
from discord.ext import commands

import random, time

import datetime

from PIL import Image

allAgentsByRoleRanked = [
    {
        'Pheonix': 2,
        'Jett': 5,
        'Raze': 4,
        'Reyna': 4,
        'Yoru': 3,
        'Neon': 2
    },
    {
        'Brimstone': 5,
        'Viper': 3,
        'Omen': 4,
        'Astra': 3,
        'Harbor': 2
    },
    {
        'Cypher': 5,
        'Sage': 3,
        'Chamber': 4,
        'Killjoy': 6
    },
    {
        'Sova': 5,
        'Skye': 5,
        'Kay/o': 6,
        'Breach': 3,
        'Fade': 6,
        'Gekko': 5
    }]
allAgents = ["Pheonix", "Jett", "Raze", "Reyna", "Yoru", "Neon", "Brimstone", "Viper", "Omen", "Astra", "Cypher",
             "Sage", "Chamber", "Killjoy", "Sova", "Skye", "Kay/o", "Breach", "Fade", "Harbor", "Gekko"]


def choice_excluding(lst, exception):
    possible_choices = [v for v in lst if v != exception]
    return random.choice(possible_choices)


def randomAgentFromDict(dict):
    agent = random.choices(population=list(dict.keys()), k=1, weights=list(dict.values()))
    for i in agent:
        return i


def randTeamComp():
    teamComp = []
    chosenAgent = random.choice(allAgents)
    while len(teamComp) < 5:
        teamComp.append(chosenAgent)
        for dicti in allAgentsByRoleRanked:
            if (chosenAgent in dicti.keys()):
                chosenDictionary = choice_excluding(allAgentsByRoleRanked, dicti)
        chosenAgent = randomAgentFromDict(chosenDictionary)
        while (chosenAgent in teamComp):
            chosenAgent = randomAgentFromDict(chosenDictionary)
    banner = []
    for elements in teamComp:
        if (elements == 'Brimstone'):
            banner.append("Brimstone.png")
        elif (elements == 'Astra'):
            banner.append("Astra.png")
        elif (elements == 'Cypher'):
            banner.append("Cypher.png")
        elif (elements == 'Chamber'):
            banner.append("Chamber.png")
        elif (elements == 'Breach'):
            banner.append("Breach.png")
        elif (elements == 'Jett'):
            banner.append("Jett.png")
        elif (elements == 'Kay/o'):
            banner.append("Kayo.png")
        elif (elements == 'Killjoy'):
            banner.append("Killjoy.png")
        elif (elements == 'Neon'):
            banner.append("Neon.png")
        elif (elements == 'Omen'):
            banner.append("Omen.png")
        elif (elements == 'Pheonix'):
            banner.append("Pheonix.png")
        elif (elements == 'Raze'):
            banner.append("Raze.png")
        elif (elements == 'Reyna'):
            banner.append("Reyna.png")
        elif (elements == 'Sage'):
            banner.append("Sage.png")
        elif (elements == 'Skye'):
            banner.append("Skye.png")
        elif (elements == 'Sova'):
            banner.append("Sova.png")
        elif (elements == 'Viper'):
            banner.append("Viper.png")
        elif (elements == 'Yoru'):
            banner.append("Yoru.png")
        elif (elements == 'Fade'):
            banner.append("Fade.png")
        elif (elements == 'Harbor'):
            banner.append("Harbor.png")
        elif (elements == 'Gekko'):
            banner.append("Gekko.png")

    frame = Image.open('rtcImages/FinalFrame.png')
    # 1 = 66,104 2 = 254,104 3 = 441,104 4 = 629,104 5 = 816,104
    banner1 = Image.open("rtcImages/" + ''.join(banner[0]))
    banner2 = Image.open("rtcImages/" + ''.join(banner[1]))
    banner3 = Image.open("rtcImages/" + ''.join(banner[2]))
    banner4 = Image.open("rtcImages/" + ''.join(banner[3]))
    banner5 = Image.open("rtcImages/" + ''.join(banner[4]))
    banner1 = banner1.resize((145, 338))
    banner2 = banner2.resize((145, 338))
    banner3 = banner3.resize((145, 338))
    banner4 = banner4.resize((145, 338))
    banner5 = banner5.resize((145, 338))
    frame.paste(banner1, (63, 114))
    frame.paste(banner2, (251, 114))
    frame.paste(banner3, (439, 114))
    frame.paste(banner4, (627, 114))
    frame.paste(banner5, (815, 114))
    frame.save("rtcImages/sentcomp.png")
    banner.clear()


class rtc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # commandGoesHere
    @app_commands.command(name="rtc", description="Random Team Comp Generator")
    async def rtc(self, interaction: discord.Interaction):
        await interaction.response.send_message(file=discord.File("rtcImages/sentcomp.png"))
        randTeamComp()
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(rtc(bot))