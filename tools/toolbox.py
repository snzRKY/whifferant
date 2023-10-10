import sqlite3 as sql
import csv
serverBasedInv = sql.connect("./db/serverBasedInv.db")
cursor = serverBasedInv.cursor()


#Displays All Items In serverBasedInv.db related to the table userInv
def display():
  cursor.execute("CREATE TABLE IF NOT EXISTS userInv(userId integer,serverId integer,inventory string)")
  selection = cursor.execute("SELECT * FROM userInv")
  for user in selection:
    print(user)


def load_line(header,line):
  tempDict = {}
  for i in range(len(header)):
    tempDict[header[i]] = line[i]
  return tempDict

def load_data(csvFile):
  outList = []
  with open(csvFile) as someFile:
    reader = csv.reader(someFile)
    header = next(reader)
    for lines in reader:
      outList.append(load_line(header,lines))
  return outList

def listOutCsv(csvFile):
  out = []
  with open("./csv/" + csvFile) as someFile:
    reader = csv.reader(someFile)
    next(reader)
    for lines in reader:
      for b in lines:
        out.append(b)
  return out

def emojiFinder(key):
  with open("./csv/itemEmojis.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for lines in reader:
      if(lines[0] == key):
        return lines[1]
    return ":x:"