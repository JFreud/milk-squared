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
    cm = "CREATE TABLE IF NOT EXISTS players (gameID INTEGER, userID INTEGER, dead INTEGER, targetID INTEGER, totalKills INTEGER);"
    c.execute(cm)
    cm = "CREATE TABLE IF NOT EXISTS kills (gameID INTEGER, userKilledID INTEGER, userWhoKilledID INTEGER, confirmed INTEGER, dateKilled TEXT, timeKilled TEXT);"
    c.execute(cm)
    cm = "CREATE TABLE IF NOT EXISTS rules (gameID INTEGER, type INTEGER, maxPeople INTEGER, safeZones TEXT);"
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
    cm = 'INSERT INTO players VALUES (%d, %d, 0, -1, 0);' %(gameID, userID)
    c.execute(cm)
    closeDatabase(db)

def leaveGame(userID, gameID):
    #removes player from game
    db, c = openDatabase()
    cm = 'DELETE FROM players WHERE gameID == %d and userID == %d;' %(gameID, userID)
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
    cm = "SELECT * FROM players WHERE gameID = %d AND dead = 0" %gameID
    listy = []
    for i in c.execute(cm):
        listy.append(i[1])
    closeDatabase(db)
    return listy

def getFinishedGames():
    db, c = openDatabase()
    cm = "SELECT gameID FROM games WHERE started = 2" 
    listy = []
    for i in c.execute(cm):
        listy.append(i[0])
    closeDatabase(db)
    return listy

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

# GAME PROGRESSION

def startgame(gameID):
    db, c = openDatabase()
    cm = 'UPDATE games SET started = 1 WHERE gameID == %d' %gameID
    c.execute(cm)
    closeDatabase(db)

def endgame(gameID):
    db, c = openDatabase()
    cm = 'UPDATE games SET started = 2 WHERE gameID == %d' %gameID
    c.execute(cm)
    closeDatabase(db)

#ALL THE KILLING STUFF

def killTarget(userID, targetID, gameID, time, date):
    db, c = openDatabase()
    if alreadySubmitted(userID, targetID, gameID):
        confirmKill(userID, gameID, targetID)
        returned = True
    else:
        cm = 'INSERT INTO kills VALUES(%d, %d, %d, %d, "%s", "%s");' % (gameID, targetID, userID, 0, date, time)
        c.execute(cm)
        returned = False
    closeDatabase(db)
    return returned

def confirmKill(userID, gameID, targetID):
    db, c = openDatabase()
    cm = 'UPDATE kills SET confirmed = 1 WHERE userWhoKilledID == %d AND gameID == %d;' % (userID, gameID)
    c.execute(cm)
    closeDatabase(db)
    db, c = openDatabase()
    targetsquared = getTarget(targetID, gameID, True)
    if (targetsquared == userID):
        #user won the game
        pass
    else:
        setTarget(userID, gameID, targetsquared)
    cm = 'UPDATE players SET totalkills = totalkills + 1 WHERE userID == %d AND gameID == %d;' % (userID, gameID)
    c.execute(cm)
    cm = 'UPDATE players SET dead = 1 WHERE userID == %d AND gameID == %d;' % (targetID, gameID)
    c.execute(cm)
    closeDatabase(db)

def alreadySubmitted(userID, targetID, gameID):
    db, c = openDatabase()
    cm = "SELECT * FROM kills WHERE userWhoKilledID == %d AND userKilledID == %d AND gameID == %d;" %(userID, targetID, gameID)
    x = False
    for i in c.execute(cm):
        x = True
    closeDatabase(db)
    return x

if __name__ == "__main__":
    createDatabase()
    #register("la","la234","lala")
