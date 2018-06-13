import sqlite3
import os
import datetime

# DATABASE CREATION/EDITING
def createDatabase():
    db, c = openDatabase()
    cm = "CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, username TEXT, password BLOB, name TEXT, extension TEXT);"
    c.execute(cm)
    cm = "CREATE TABLE IF NOT EXISTS games (gameID INTEGER PRIMARY KEY, managerID INTEGER, key TEXT, type INTEGER, dateStart TEXT, dateEnd TEXT, title TEXT, description TEXT, started INTEGER);"
    c.execute(cm)
    cm = "CREATE TABLE IF NOT EXISTS players (gameID INTEGER, userID INTEGER, dead INTEGER, targetID INTEGER, totalKills INTEGER, submitted INTEGER, place INTEGER);"
    c.execute(cm)
    cm = "CREATE TABLE IF NOT EXISTS kills (gameID INTEGER, userKilledID INTEGER, userWhoKilledID INTEGER, confirmed INTEGER, dateKilled TEXT, timeKilled TEXT);"
    c.execute(cm)
    cm = "CREATE TABLE IF NOT EXISTS rules (gameID INTEGER, type INTEGER, maxPeople INTEGER, safeZones TEXT);"
    c.execute(cm)
    cm = "CREATE TABLE IF NOT EXISTS feed (gameID INTEGER, message INTEGER);"
    c.execute(cm)
    closeDatabase(db)

def openDatabase():
    f = os.path.dirname(__file__) + "/../data/database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    return db, db.cursor()    #facilitate db ops

def closeDatabase(db):
    db.commit() #save changes
    db.close()  #close database

# FUNCTIONS!!!


# AUTHENTICATION
def checkUsernames(username):
    #checks if username is taken
    #returns True if username is taken, returns False if username is not taken
    db, c = openDatabase()
    cm = "SELECT * FROM users WHERE username=='"+ username +"';"
    for i in c.execute(cm):
        #if username == i[0].encode("ascii"):
            #closeDatabase(db)
        return True
    closeDatabase(db)
    return False

def register(username, password, name):
    #adds a new record in the users table with the username, password, name, and a userID (found in function)
    db, c = openDatabase()
    cm = "SELECT COUNT(*) FROM users;"
    for i in c.execute(cm):
        userID = i[0]
    c.execute("INSERT INTO users VALUES(?,?,?,?,?)",[userID, username, password, name,'jpg'])
    closeDatabase(db)

def verify(username, password):
    #checks whether a person's password matches their username
    db, c = openDatabase()
    cm = 'SELECT password FROM users WHERE username == "%s";' %username
    x = c.execute(cm)
    for i in x:
        true_pass = i
    closeDatabase(db)
    return password == true_pass[0].encode("ascii")

def changeAccountSettings(username, changed, column):
    #changes a user's account settings
    db, c = openDatabase()
    cm = 'UPDATE users SET %s = "%s" WHERE username == "%s";' %(column, changed, username)
    c.execute(cm)
    closeDatabase(db)

# GAME MANAGEMENT
def crGame(adminID, key, typ, startDate, endDate, title, descr):
    #creates a game in the games table
    db, c = openDatabase()
    cm = "SELECT COUNT(*) FROM games;"
    for i in c.execute(cm):
        gameID = i[0]
    cm = 'INSERT INTO games VALUES(%d, %d, "%s", "%s", "%s", "%s", "%s", "%s", 0);' %(gameID, adminID, key, typ, startDate, endDate, title, descr)
    c.execute(cm)
    closeDatabase(db)
    return gameID

def deleteGame(gameID):
    db, c = openDatabase()
    cm = "DELETE FROM games WHERE gameID == %d" %gameID
    c.execute(cm)
    cm = "DELETE FROM players WHERE gameID == %d" %gameID
    c.execute(cm)
    closeDatabase(db)

def crRules(gameID, typ, maxPeople, safeZones):
    db, c = openDatabase()
    cm = 'INSERT INTO rules VALUES (%d, %d, %d, "%s");' %(gameID, typ, maxPeople, safeZones)
    c.execute(cm)
    closeDatabase(db)

def checkKey(key):
    db, c = openDatabase()
    cm = 'SELECT gameID FROM games WHERE key == "%s";' %key
    game = "doesn't exist"
    for i in c.execute(cm):
        game = i[0]
    closeDatabase(db)
    return game

def joinGame(gameID, userID):
    #adds player into a game
    db, c = openDatabase()
    cm = 'INSERT INTO players VALUES (%d, %d, 0, -1, 0, 0, 0);' %(gameID, userID)
    c.execute(cm)
    cm = 'INSERT INTO feed VALUES (%d, "%s has joined the game.");' %(gameID, getUsername(userID))
    c.execute(cm)
    closeDatabase(db)

def leaveGame(userID, gameID):
    #removes player from game
    db, c = openDatabase()
    cm = 'DELETE FROM players WHERE gameID == %d and userID == %d;' %(gameID, userID)
    c.execute(cm)
    cm = 'INSERT INTO feed VALUES (%d, "%s has left the game.");' %(gameID, getUsername(userID))
    c.execute(cm)
    closeDatabase(db)

def changeGameSettings(gameID, changed, column):
    db, c = openDatabase()
    if column == "maxPeople":
        cm = 'UPDATE rules SET %s = %d WHERE gameID = %d;' %(column, changed, gameID)
    elif column == "safeZones":
        cm = 'UPDATE rules SET %s = "%s" WHERE gameID = %d;' %(column, changed, gameID)
    elif column == "startDate":
        cm = 'UPDATE games SET dateStart = "%s" WHERE gameID = %d;' %(changed, gameID)
    elif column == "endDate":
        cm = 'UPDATE games SET dateEnd = "%s" WHERE gameID = %d;' %(changed, gameID)
    else:
        cm = 'UPDATE games SET %s = "%s" WHERE gameID = %d;' %(column, changed, gameID)
    c.execute(cm)
    cm = 'INSERT INTO feed VALUES(%d, "The admin has updated the %s.");' (gameID, column)
    closeDatabase(db)

# END FUNCTIONS



# START ALL OUR GETTERS AND SETTERS

def getUserID(username):
    db, c = openDatabase()
    cm = 'SELECT userID FROM users WHERE username == "%s";' %username
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def getExtension(userID):
    db, c = openDatabase()
    cm = 'SELECT extension FROM users WHERE userID == %d;' % userID
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def setExtension(userID, extension):
    db, c = openDatabase()
    cm = 'UPDATE users SET extension = "%s" WHERE userID == %d;' % (extension, userID)
    c.execute(cm)
    closeDatabase(db)

def getUsername(userID):
    db, c = openDatabase()
    cm = 'SELECT username FROM users WHERE userID == %d;' %userID
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def getName(username):
    db, c = openDatabase()
    cm = 'SELECT name FROM users WHERE username == "%s";' %username
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def getNameFromID(userID):
    db, c = openDatabase()
    cm = 'SELECT name FROM users WHERE userID == %d;' %userID
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def getTarget(userID, gameID, boo):
    db, c = openDatabase()
    if boo:
        cm = 'SELECT targetID FROM players WHERE userID == %d AND gameID == %d;' %(userID, gameID)
        x = -2
        for i in c.execute(cm):
            x = i[0]
    else:
        cm = 'SELECT userID FROM players WHERE targetID == %d AND gameID == %d;' %(userID, gameID)
        for i in c.execute(cm):
            x = i[0]
    closeDatabase(db)
    return x

def setTarget(userID, gameID, targetID):
    db, c = openDatabase()
    cm = 'UPDATE players SET targetID = %d WHERE userID == %d AND gameID == %d;' %(targetID, userID, gameID)
    c.execute(cm)
    closeDatabase(db)

def setNewTarget(userID, gameID, targetID, db, c):
    cm = 'UPDATE players SET targetID = %d WHERE userID == %d AND gameID == %d;' %(targetID, userID, gameID)
    c.execute(cm)

def getPlayers(gameID):
    db, c = openDatabase()
    cm = 'SELECT userID FROM players WHERE gameID == %d;' %gameID
    listy0 = []
    listy1 = []
    for i in c.execute(cm):
        listy0.append(i[0])
        listy1.append(getName(getUsername(i[0])))
    closeDatabase(db)
    return listy0, listy1

def getGameStats(gameID):
    db, c = openDatabase()
    cm = 'SELECT * FROM gamestats WHERE gameID == %d;' %gameID
    listy = []
    for i in c.execute(cm):
        listy.append(i[0])
    closeDatabase(db)
    return listy[1:]

def getLifetimeStats(userID):
    db, c = openDatabase()
    cm = 'SELECT * FROM userstats WHERE userID == %d;' %userID
    listy = []
    for i in c.execute(cm):
        listy.append(i[0])
    closeDatabase(db)
    return listy[1:]

def getGames(userID):
    db, c = openDatabase()
    cm = 'SELECT * FROM games WHERE managerID == %d;' %userID
    listy = []
    for i in c.execute(cm):
        if getMaxPlayers(i[0]) != -1:
            listy.append(i[6])
    closeDatabase(db)
    return listy

def getGamesID(userID):
    db, c = openDatabase()
    cm = 'SELECT * FROM games WHERE managerID == %d;' %userID
    listy = []
    for i in c.execute(cm):
        if getMaxPlayers != -1:
            listy.append(i[0])
    closeDatabase(db)
    return listy

def getTitle(gameID):
    db, c = openDatabase()
    cm = 'SELECT * FROM games WHERE gameID == %d;' %gameID
    for i in c.execute(cm):
        closeDatabase(db)
        return i[6]

def getPlaying(userID):
    db, c = openDatabase()
    cm = 'SELECT * FROM players WHERE userID == %d;' %userID
    listy1 = []
    listy2 = []
    for i in c.execute(cm):
        listy1.append(getTitle(i[0]))
        listy2.append(i[0])
    closeDatabase(db)
    return listy1, listy2

def getPlayersAlive(gameID):
    db, c = openDatabase()
    cm = "SELECT * FROM players WHERE gameID == %d AND dead == 0;" %gameID
    listy = []
    for i in c.execute(cm):
        listy.append(i[1])
    closeDatabase(db)
    return listy

def getRemaining(gameID, db, c):
    cm = "SELECT * FROM players WHERE gameID == %d AND dead == 0;" %gameID
    listy = []
    for i in c.execute(cm):
        listy.append(i[1])
    return listy

def getFinishedGames():
    db, c = openDatabase()
    cm = "SELECT gameID FROM games WHERE started == 2;"
    listy = []
    for i in c.execute(cm):
        listy.append(i[0])
    closeDatabase(db)
    return listy

def getSubmitted(userID, gameID):
    db, c = openDatabase()
    cm = 'SELECT submitted FROM players WHERE gameID == %d AND userID == %d;' %(gameID, userID)
    x = -1
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def getGameType(gameID):
    db, c = openDatabase()
    cm = 'SELECT type FROM games WHERE gameID == %d' % gameID
    x = -1
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def getMaxPlayers(gameID):
    db, c = openDatabase()
    cm = "SELECT maxPeople FROM rules WHERE gameID == %d" %gameID
    x = -1
    try:
        for i in c.execute(cm):
            x = i[0]
    except:
        x = -1
    closeDatabase(db)
    return x

def getGameInfo(gameID):
    db, c = openDatabase()
    cm = 'SELECT * FROM games WHERE gameID == %d;' %gameID
    returned = {}
    stuff = ["gameID", "managerID", "key", "type", "dateStart", "dateEnd", "title", "description", "started"]
    x = list(c.execute(cm))[0]
    for i in range(0, len(x)):
        returned[stuff[i]] = x[i]
    cm = 'SELECT * FROM rules WHERE gameID == %d;' %gameID
    stuff = [0, "type", "maxNumOfPeople", "safeZones"]
    x = list(c.execute(cm))[0]
    for i in range(1, len(x)):
        returned[stuff[i]] = x[i]
    closeDatabase(db)
    return returned

def getFeed(gameID):
    db, c = openDatabase()
    cm = 'SELECT message FROM feed WHERE gameID == %d;' %gameID
    listy = []
    for i in c.execute(cm):
        listy.append(i[0])
    closeDatabase(db)
    return listy[::-1]


# GAME PROGRESSION

def startgame(gameID):
    db, c = openDatabase()
    cm = 'UPDATE games SET started = 1 WHERE gameID == %d' %gameID
    c.execute(cm)
    cm = 'INSERT INTO feed VALUES (%d, "The game has started.");' %(gameID)
    c.execute(cm)
    closeDatabase(db)

def restartgame(gameID):
    db, c = openDatabase()
    cm = 'UPDATE players SET dead = 0 WHERE gameID == %d' %gameID
    c.execute(cm)
    cm = 'INSERT INTO feed VALUES (%d, "Targets have been reassigned.");' %(gameID)
    c.execute(cm)
    closeDatabase(db)

def endgame(gameID):
    db, c = openDatabase()
    cm = 'UPDATE games SET started = 2 WHERE gameID == %d' %gameID
    c.execute(cm)
    cm = 'INSERT INTO feed VALUES (%d, "The game has ended.");' %(gameID)
    c.execute(cm)
    closeDatabase(db)

def makeAnnouncement(gameID, announcement):
    db, c = openDatabase()
    cm = 'INSERT INTO feed VALUES (%d, "%s");' %(gameID, announcement)
    c.execute(cm)
    closeDatabase(db)

#ALL THE KILLING STUFF

def killTarget(userID, targetID, gameID, time, date):
    db, c = openDatabase()
    if alreadySubmitted(userID, targetID, gameID, db, c):
        confirmKill(userID, gameID, targetID, db, c)
        returned = True
    else:
        cm = 'INSERT INTO kills VALUES(%d, %d, %d, %d, "%s", "%s");' % (gameID, targetID, userID, 0, date, time)
        c.execute(cm)
        cm = 'UPDATE players SET submitted = 1 WHERE userID == %d AND gameID == %d;' %(userID, gameID)
        c.execute(cm)
        returned = False
    closeDatabase(db)
    return returned

def confirmKill(userID, gameID, targetID, db, c):
    # LEAVE THESE OPEN DB LINES COMMENTED!!! YOU CAN ONLY OPEN A DB ONCE AND HAVE TO CLOSE BEFORE OPENING AGAIN!
    # db, c = openDatabase()
    cm = 'UPDATE kills SET confirmed = 1 WHERE userWhoKilledID == %d AND gameID == %d;' % (userID, gameID)
    c.execute(cm)
    # closeDatabase(db)
    # db, c = openDatabase()
    targetsquared = getTarget(targetID, gameID, True)
    cm = 'UPDATE players SET totalkills = totalkills + 1 WHERE userID == %d AND gameID == %d;' % (userID, gameID)
    c.execute(cm)
    cm = 'UPDATE players SET dead = 1 WHERE userID == %d AND gameID == %d;' % (targetID, gameID)
    c.execute(cm)
    cm = 'UPDATE players SET submitted = 0 WHERE userID == %d AND gameID == %d;' % (targetID, gameID)
    c.execute(cm)
    cm = 'UPDATE players SET submitted = 0 WHERE userID == %d AND gameID == %d;' % (userID, gameID)
    c.execute(cm)
    cm = 'INSERT INTO feed VALUES (%d, "%s killed %s.");' %(gameID, getUsername(userID), getUsername(targetID))
    c.execute(cm)
    playersLeft = len(getRemaining(gameID, db, c))
    cm = 'UPDATE players SET place = %d WHERE userID == %d;' % (playersLeft + 1, targetID)
    c.execute(cm)
    if (targetsquared == userID):
        cm = 'INSERT INTO feed VALUES (%d, "The winner is %d.");' %(gameID, db.getUsername(userID))
        c.execute(cm)
        cm = 'UPDATE players SET place = 1 WHERE userID == %d;' % userID
        c.execute(cm)
    else:
        setNewTarget(userID, gameID, targetsquared, db, c)
    # closeDatabase(db)


def alreadySubmitted(userID, targetID, gameID, db, c):
    # db, c = openDatabase()
    cm = "SELECT * FROM kills WHERE userWhoKilledID == %d AND userKilledID == %d AND gameID == %d;" %(userID, targetID, gameID)
    x = False
    for i in c.execute(cm):
        x = True
    # closeDatabase(db)
    return x

# PLAYER STATS STUFFS

def makeRapidFireRanking(gameID):
    db, c = openDatabase()
    listy = []
    listykills = []
    cm = "SELECT userID, totalkills FROM players WHERE gameID == %d ORDER BY totalKills;" % (gameID)
    for i in c.execute(cm):
        listy.append(i[0]) # appends userID in order of totalkills
        listykills.append(i[1])
    closeDatabase(db)
    return listy, listykills


#total kills of a player across all games
def getTotalKills():
    totalDict = dict()
    db, c = openDatabase()
    cm = "SELECT * FROM players;"
    for i in c.execute(cm):
        if i[1] in totalDict:
            totalDict[i[1]] += i[4] #adds kills from that game to total
        else:
            totalDict[i[1]] = i[4] #creates entry and sets kills equal to game total
    closeDatabase(db)
    return totalDict

#total games played of a player
def getNumGamesPlayed():
    totalDict = dict()
    db, c = openDatabase()
    cm = "SELECT * FROM players;"
    for i in c.execute(cm):
        if i[1] in totalDict:
            totalDict[i[1]] += 1 #adds one to a user's game count
        else:
            totalDict[i[1]] = 1 #creates game count and sets games = to 1
    closeDatabase(db)
    return totalDict

#highest kills gotten in a game
def getRecordKills():
    recordDict = dict()
    db, c = openDatabase()
    cm = "SELECT * FROM players;"
    for i in c.execute(cm):
        if i[1] in recordDict:
            if i[4] > recordDict[i[1]]:
                recordDict[i[1]] = i[4]
        else:
            recordDict[i[1]] = i[4]
    closeDatabase(db)
    return recordDict

#average kills per game of a player
def getAverageKills(userID):
    killTotal = float(getTotalKills()[userID])
    gamesPlayed = float(getNumGamesPlayed()[userID])
    return killTotal / gamesPlayed

#number of games a player has won
def getNumGamesWon(userID):
    #count number of games where everyone else is dead and you are not
    totalDict = dict()
    db, c = openDatabase()
    cm = "SELECT * FROM players;"
    gameID = 0
    winner = False
    for i in c.execute(cm):
        # if i[0] == gameID and i[2] == 0 and winner == False:
        #     winner == True
        # elif i[0] == gameID and i[2] == 0 and winner == True:
        #     winner == False
        pass
    return


#GAME STATS STUFF

def getGameKills(gameID):
    killDict = dict()
    newDict = dict()
    db, c = openDatabase()
    cm = "SELECT * FROM players;"
    for i in c.execute(cm):
        if i[0] == gameID:
            killDict[i[1]] = i[4] #creates entry and sets kills equal to game total
    closeDatabase(db)
    for key in killDict:
        newDict[getNameFromID(int(key))] = killDict[key]
    return newDict


if __name__ == "__main__":
    createDatabase()
    #testing player stat functions
    # print getTotalKills()
    # print getNumGamesPlayed()
    # print getRecordKills()
    # print getAverageKills(1)
    #register("la","la234","lala")
