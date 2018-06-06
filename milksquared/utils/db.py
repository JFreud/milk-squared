import sqlite3
import os

# DATABSE CREATION/EDITING
def createDatabase():
    db, c = openDatabase()
    cm = "CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, username TEXT, password BLOB, name TEXT);"
    #for i in userStatList():
        #cm += ", " + i[0] + " " + i[1]
    c.execute(cm)
    cm = "CREATE TABLE IF NOT EXISTS games (gameID INTEGER PRIMARY KEY, managerID INTEGER, key TEXT, type INTEGER, dateStart TEXT, dateEnd TEXT, title TEXT, description TEXT);"
    #for i in rulesForGame():
        #cm += ", " + i[0] + " " + i[1]
    #for i in gameStatList():
        #cm += ", " + i[0] + " " + i[1]
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

def gameStatList():
    return [["numberLeft", "INTEGER"], ["totalKills", "INTEGER"], ["mostKillsPerDay", "TEXT"], ["mostKillsTotal", "TEXT"], ["mostKillsToday", "TEXT"]]

def userStatList():
    return [["averageKillsPerGame", "REAL"], ["averageDailyKills", "REAL"]]

def rulesForGame():
    return [["maxNumOfPeople", "INTEGER"], ["safeZones", "TEXT"]]





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
    c.execute("INSERT INTO users VALUES(?,?,?,?)",[userID, username, password, name])
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

def changePass(username, oldPass, newPass):
    #changes a user's password
    #returns True
    db, c = openDatabase()
    cm = 'UPDATE users SET password = "%s" WHERE username == "%s";' %(newPass, username)
    c.execute(cm)
    closeDatabase(db)
    return True




# GAME MANAGEMENT
def crGame(adminID, key, typ, startDate, endDate, title, descr):
    #creates a game in the games table
    db, c = openDatabase()
    cm = "SELECT COUNT(*) FROM games;"
    for i in c.execute(cm):
        gameID = i[0]
    cm = 'INSERT INTO games VALUES(%d, %d, "%s", "%s", "%s", "%s", "%s", "%s");' %(gameID, adminID, key, typ, startDate, endDate, title, descr)
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

# END FUNCTIONS



# START ALL OUR GETTERS AND SETTERS

def getUserID(username):
    db, c = openDatabase()
    cm = 'SELECT userID FROM users WHERE username == "%s";' %username
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

def getTarget(userID, gameID):
    db, c = openDatabase()
    cm = 'SELECT target FROM players WHERE userID == %d AND gameID == %d;' %(userID, gameID)
    for i in c.execute(cm):
        x = i[0]
    closeDatabase(db)
    return x

def setTarget(userID, gameID, targetID):
    db, c = openDatabase()
    cm = 'UPDATE players SET target = %d WHERE userID == %d AND gameID == %d;' %(targetID, userID, gameID)
    c.execute(cm)
    closeDatabase(db)

def getPlayers(gameID):
    db, c = openDatabase()
    cm = 'SELECT userID FROM players WHERE gameID == %d;' %gameID
    listy = []
    for i in c.execute(cm):
        listy.append(i[0])
    closeDatabase(db)
    return listy

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
        listy.append(i[6])
    closeDatabase(db)
    return listy

def getTitle(gameID):
    db, c = openDatabase()
    cm = 'SELECT * FROM games WHERE gameID == %d;' %userID
    for i in c.execute(cm):
        closeDatabase(db)
        return i[6]
    
def getPlaying(userID):
    db, c = openDatabase()
    cm = 'SELECT * FROM players WHERE userID == %d;' %userID
    listy = []
    for i in c.execute(cm):
        listy.append(getTitle(i[0]))
    closeDatabase(db)
    return listy

createDatabase()
#register("la","la234","lala")
