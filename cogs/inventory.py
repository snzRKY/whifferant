import discord
from discord import app_commands
from discord.ext import commands
import math
import numpy as np
from tools import lootboxsystem
from tools import toolbox as tb
import csv


def inventoryPageEmbed(pageInv, userName, avatarIcon):
    pageNum = pageInv[len(pageInv) - 1]
    embed = discord.Embed()
    embed.set_author(name=userName + "'s Inventory", icon_url=avatarIcon)
    embed.set_footer(text="Page: " + str(pageNum))
    for stuff in pageInv[pageNum - 1]:
        for key in stuff:
            emoji = tb.emojiFinder(key)
            embed.add_field(name=emoji + " " + key + " - " + str(stuff[key][0]), value=str(stuff[key][1]), inline=False)
        # except IndexError:
        # pass
    return embed


class inventory(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # commandGoesHere

    @app_commands.command(name="inventory", description="Display Your Inventory")
    async def inventory(self, interaction: discord.Interaction):
        inv = lootboxsystem.displayInv(interaction.user.id, interaction.guild_id)
        if (inv != "None"):
            embed = discord.Embed()
            embed.set_author(name=interaction.user.name + "'s Inventory",
                             icon_url=interaction.user.display_avatar)
            embed.set_footer(text="Page: 1")
            listInv = []
            if (inv != {}):
                for items in inv:
                    listInv.append({items: [inv[items][0], inv[items][1]]})

            totalPage = math.ceil(len(listInv) / 7)
            listPage = []
            if (totalPage != 0):
                listInv = np.array_split(listInv, totalPage)
                for i in listInv:
                    listPage.append(list(i))
                listPage.append(1)
            if (listPage == []):
                await interaction.response.send_message("You Have Nothing In Your Inventory!")
                return
            for i in range(len(listPage[0])):
                try:
                    for stuff in listPage[0]:
                        for key in stuff:
                            emoji = tb.emojiFinder(key)
                            embed.add_field(name=emoji + " " + key + " - " + str(stuff[key][0]),
                                            value=str(stuff[key][1]), inline=False)
                except IndexError:
                    pass
                view = discord.ui.View()
                pageback = discord.ui.Button(style=discord.ButtonStyle.red, label="<")
                pagefoward = discord.ui.Button(style=discord.ButtonStyle.red, label=">")

                async def pb(inter):
                    await inter.response.defer()
                    if (listPage[len(listPage) - 1] == 1):
                        pass
                    else:
                        listPage[len(listPage) - 1] -= 1
                        await interaction.edit_original_response(
                            embed=inventoryPageEmbed(listPage, interaction.user.name, interaction.user.display_avatar),
                            view=view)

                async def pf(inter):
                    await inter.response.defer()
                    if (listPage[len(listPage) - 1] >= totalPage):
                        pass
                    else:
                        listPage[len(listPage) - 1] += 1
                        await interaction.edit_original_response(
                            embed=inventoryPageEmbed(listPage, interaction.user.name, interaction.user.display_avatar),
                            view=view)

                pageback.callback = pb
                pagefoward.callback = pf
                view.add_item(pageback)
                view.add_item(pagefoward)
                sentInteraction = False
                if (sentInteraction == False):
                    sentInteraction = True
                    await interaction.response.send_message(embed=embed, view=view)
                if (totalPage == 1):
                    return
            else:
                await interaction.response.send_message("You Have Nothing In Your Inventory!")

        else:
            await interaction.response.send_message("use /signup to access this command!")
        return

    @inventory.error
    async def on_inventory_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(inventory(bot))