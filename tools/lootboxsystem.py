import sqlite3 as sql
import random
from tools import toolbox as tb

serverBasedInv = sql.connect("./db/serverBasedInv.db")
cursor = serverBasedInv.cursor()

# The inventory value in the table userInv is a dictionary
# dictionary["items"] is a dictionary, key = itemName value = amount of that item
# dictionary["credits"] is a integer, number of credits
# dictionary["boxes"] is a dictionary, key = boxName value = amount of that box

cursor.execute("CREATE TABLE IF NOT EXISTS userInv(userId integer,serverId integer,inventory string)")


# Checks if the user that signs up is already in the database
def signUpCheck(userId, serverId):
    selection = cursor.execute("SELECT * FROM userInv WHERE userId = ?", (userId,))
    for instance in selection:
        if (instance[1] == serverId):
            return False
    return True


# Adds user into the database
def signUp(userId, serverId):
    if (signUpCheck(userId, serverId)):
        cursor.execute("INSERT OR IGNORE INTO userInv VALUES (?,?,?)",
                       (userId, serverId, "{'items':{},'credits':0,'boxes':{}}"))
        serverBasedInv.commit()
        return ("Successfully Completed Signup")
    else:
        return ("User Already Completed A Signup")


# returns the inventory of the user specified
def inventory(userId, serverId):
    selection = cursor.execute("SELECT * FROM userInv WHERE userId = ? AND serverId = ?", (userId, serverId))
    for i in selection:
        if (i != None):
            return eval(i[2])
        else:
            return "None"


# Updates whole inventory
def inventoryUpdater(userId, serverId, newInventory):
    cursor.execute("UPDATE userInv SET inventory = ? WHERE userId = ? AND serverId = ?",
                   (newInventory, userId, serverId))
    serverBasedInv.commit()


# Does Item exist within the csv file under 'name'
def itemChecker(csvFile, item):
    response = tb.load_data("./csv/" + csvFile)
    for items in response:
        if (items['name'].lower() == item.lower()):
            return True
    return False


# Deletes entire Inventory
def purgeInv(userId, serverId):
    inventoryUpdater(userId, serverId, "{'items':{},'credits':0,'boxes':{}}")


def deleteItem(userId, serverId, name, amount):
    if (itemChecker('items.csv', name)):
        inv = inventory(userId, serverId)
        if (name in inv['items']):
            if (inv['items'][name] < amount):
                print('user does not own that much')
            else:
                inv['items'][name] -= amount
                if (inv['items'][name] == 0):
                    inv['items'].pop(name)
        else:
            print("user does not own this item")
        inventoryUpdater(userId, serverId, str(inv))
    else:
        print("Invalid Item")


def deleteLootbox(userId, serverId, type, amount):
    if (itemChecker('boxes.csv', type)):
        inv = inventory(userId, serverId)
        if (type in inv['boxes']):
            if (inv['boxes'][type] < amount):
                print('user does not own that much')
            else:
                inv['boxes'][type] -= amount
                if (inv['boxes'][type] == 0):
                    inv['boxes'].pop(type)
        else:
            print("user does not own this loot box")
        inventoryUpdater(userId, serverId, str(inv))
    else:
        print("Invalid Item")


def deleteCredit(userId, serverId, amount):
    inv = inventory(userId, serverId)
    if (inv['credits'] != 0) and (inv['credits'] >= amount):
        inv['credits'] -= amount
    else:
        print("User does not own that much credits!")


# Gives specific item
def giveItem(userId, serverId, name, amount):
    if (itemChecker('items.csv', name)):
        inv = inventory(userId, serverId)
        if (name in inv['items']):
            inv['items'][name] += amount
        else:
            inv['items'][name] = amount
        inventoryUpdater(userId, serverId, str(inv))
    else:
        print("Invalid Item")


def giveLootBox(userId, serverId, type, amount):
    if (itemChecker('boxes.csv', type)):
        inv = inventory(userId, serverId)
        if (inv != None):
            if (type in inv['boxes']):
                inv['boxes'][type] += amount
            else:
                inv['boxes'][type] = amount
            inventoryUpdater(userId, serverId, str(inv))
        else:
            return "None"
    else:
        print("Invalid Item")


def giveCredits(userId, serverId, amount):
    inv = inventory(userId, serverId)
    if (inv != "None"):
        inv['credits'] += amount
        inventoryUpdater(userId, serverId, str(inv))
    else:
        return "None"


def shop(userId, serverId, item):
    print("Coming Soon")


def openLootBox(userId, serverId, type, amount):
    inv = inventory(userId, serverId)
    skins = []
    test = []
    if (inv == None):
        return "User /signup to access This Command!"
    if (type in inv['boxes']):
        if (inv['boxes'][type] == {}):
            return "You have 0 Boxes Left"
        elif (inv['boxes'][type] < amount):
            return "Inefficient Amount"
        else:
            inv['boxes'][type] -= amount
            if (inv['boxes'][type] == 0):
                inv['boxes'].pop(type)
            inventoryUpdater(userId, serverId, str(inv))
            allBoxes = tb.load_data("./csv/boxes.csv")
            for i in range(amount):
                for boxes in allBoxes:
                    if (boxes['name'] == type):
                        box = tb.load_data("./csv/boxes/" + type + ".csv")
                        names = []
                        weight = []
                        for i in box:
                            names.append(i['name'])
                            weight.append(int(i['weight']))
                        skins.append(random.choices(names, weights=weight)[0])
    else:
        return "You don't own this Lootbox"
    for item in skins:
        giveItem(userId, serverId, item, 1)
    return skins


def displayInv(userId, serverId):
    inv = inventory(userId, serverId)
    if (inv == None):
        return "None"
    out = {}
    for i in inv['items']:
        out[i] = [inv['items'][i], "Skin"]
    for b in inv['boxes']:
        out[b] = [inv['boxes'][b], "Loot Box"]
    return out


serverBasedInv.commit()
tb.display()


