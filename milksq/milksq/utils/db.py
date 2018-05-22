def createDatabase():
    db, c = openDatabase()
    cm = "CREATE TABLE users ()"
    cm = "CREATE TABLE games ()"

def openDatabase():
    f="../data/database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    return db, db.cursor()    #facilitate db ops

def closeDatabase(db):
    db.commit() #save changes
    db.close()  #close database

def gameStatList():
    return []

def userStatList():
    return []

# FUNCTIONS!!!

def checkUsernames(username):
    #checks if username is taken
    #returns True if username is taken, returns False if username is not taken
    db, c = openDatabase()
    cm = "SELECT user FROM users;"
    for i in c.execute(cm):
        if username == i[0].encode("ascii"):
            closeDatabase(db)
            return True
    closeDatabase(db)
    return False

def register(username, password, name): 
    #adds a new record in the users table with the username, password, name, and a userID (found in function)
    db, c = openDatabase()
    cm = "SELECT COUNT(*) FROM users;"
    for i in c.execute(cm):
        userID = i[0]
    cm = 'INSERT INTO users VALUES("%s", "%s", %d, "%s", "");' %(username, password, userID, name)
    c.execute(cm)
    closeDatabase(db)

def verify(username, password):
    #checks whether a person's password matches their username
    db, c = openDatabase()
    cm = 'SELECT password FROM users WHERE user == "%s";' %username
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

def crGame(adminID, key, typ, startDate, endDate, title, descr):
    #creates a game in the games table
    db, c = openDatabase()
    cm = "SELECT COUNT(*) FROM games;"
    for i in c.execute(cm):
        gameID = i[0]
    cm = 'INSERT INTO games VALUES(%d, %d, "%s", "%s", %d, "%s", "%s", "%s", "%s");' %(gameID, adminID, key, typ, startDate, endDate, title, descr)
    c.execute(cm)
    closeDatabase()

def deleteGame(gameID):
    db, c = openDatabase()
    cm = "DELETE FROM games WHERE gameID == %d" %gameID
    c.execute(cm)
    cm = "DELETE FROM players WHERE gameID == %d" %gameID
    c.execute(cm)
    closeDatabase()

# END FUNCTIONS



# START ALL OUR GETTERS AND SETTERS

def getUserID(username):
    db, c = openDatabase()
    cm = 'SELECT userID FROM users WHERE username == "%s";' %username
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

