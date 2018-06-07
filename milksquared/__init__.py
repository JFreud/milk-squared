from flask import Flask, render_template, request, session, redirect, url_for, flash
from os import path, urandom
from utils import db
import random
import json, urllib2, sys, sqlite3

my_app = Flask(__name__)
my_app.secret_key = 'i dont have a secret key'

DIR = path.dirname(__file__)
#console output will appear in /var/log/apache2/error.log

# ==================== HOME =======================
# If logged in displays home/feed
# If not, redirects to login page

@my_app.route('/')
def root():
    log_status = 'user' in session
    # return render_template("login.html")
    return render_template('home.html', loggedin=log_status )


# ==================== CREATE ACCOUNT =======================
@my_app.route('/register', methods=['GET','POST'])
# Account creation (duh)
def register():
    # do db stuff and make account
    #if request.method == "GET":
    return render_template('register.html', loggedin=False)
    '''else:
        user = request.form['username']
        passw = request.form['password']

        conf = request.form['confirm']
        print user, name, passw, conf
        if not passw == conf:
            flash("Passwords do not match.")
            return render_template('register.html')
        if not db.checkUsernames(user):
            db.register(user,passw,name)
            return redirect(url_for('login'))'''



@my_app.route('/user_creation', methods=['POST'])
def user_creation():
    user = request.form['username']
    pw = request.form['password']
    pw_confirm = request.form['confirm']
    name = request.form['name']
    if db.checkUsernames(user):
        flash("Username already exists.")
        return redirect(url_for('register'))
    elif not pw == pw_confirm:
        flash("Passwords do not match.")
        return redirect(url_for('register'))
    else:
        db.register(user,pw,name)
        return redirect(url_for('login'))


# ==================== LOGIN =======================
# Login Page

@my_app.route('/login', methods=['GET','POST'])
def login():
    if "user" in session:
        return redirect(url_for('root'))
    if request.method == "GET":
        return render_template('login.html', loggedin=False)
    else:
        user = request.form['username']
        passw = request.form['password']
        if not db.checkUsernames(user) :
            flash("Invalid username")
            return redirect(url_for('login'))
        elif not db.verify(user,passw):
            flash("Invalid password")
            return redirect(url_for('login'))
        else:
            session['user'] = user
            return redirect(url_for('root'))

@my_app.route('/logout')
def logout():
    if "user" in session:
        username = session.pop('user')
        return redirect(url_for('root'))
    else:
        return redirect(url_for('root'))


# ==================== CREATE GAME =======================
# Page for the user to create the game
# Enters all the game info and stuff
# Form fields: ...

#The form
@my_app.route('/mkgame')
def mkgame():
   if "user" not in session:
       return redirect(url_for('login'))
   # elif request.method == "POST":
   #     username = session['user']
   #     gameMode = request.form['gameMode']
   #     startDate = request.form['startDate']
   #     endDate = request.form['endDate']
   #     adminID = db.getUserID(username)
   #     joinKey = request.form['joinKey']
   #     title = request.form['title']
   #     description = request.form['description']
   #     db.crGame(adminID, joinKey, gameMode, startDate, endDate, title, description)
   #     return redirect(url_for('profile'))
   else:
       return render_template("mkgame.html", loggedin=True)


#This one actually makes it
@my_app.route('/game_creation', methods=["POST"])
def create_game():
    if "user" not in session:
       return redirect(url_for('login'))
    username = session['user']
    gameMode = request.form['gameMode']
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    adminID = db.getUserID(username)
    joinKey = generateKey()
    title = request.form['title']
    description = request.form['description']
    if gameMode == "Assassins - Rapid Fire":
        typ = 0
    elif gameMode == "Assassins - Last Man Standing":
        typ = 1
    gameID = db.crGame(adminID, joinKey, gameMode, startDate, endDate, title, description)
    session['game'] = gameID
    session["gameType"] = typ
    return render_template("rules.html", gameType = typ, loggedin=True)

def generateKey():
    alphabet = []
    for letter in range(65, 91):
        alphabet.append(chr(letter))
    for letter in range(97, 123):
        alphabet.append(chr(letter))
    key = ""
    for i in range(0, 10):
        key += random.choice(alphabet)
    return key

@my_app.route('/rule_creation', methods=["POST"])
def create_rules():
    if "user" not in session:
        return redirect(url_for('login'))
    if "game" not in session or "gameType" not in session:
        flash("Please try making your game again.")
        return redirect(url_for("profile"))
    if "maxPeople" in request.form:
        gameMode = session['gameType']
        gameID = session["game"]
        maxPeople = int(request.form['maxPeople'])
        safeZones = request.form['safeZones']
        db.crRules(session["game"], gameMode, maxPeople, safeZones)
    else:
        db.deleteGame(session["game"])
    return redirect(url_for('profile'))

# ==================== GAME =======================
# Main game page that will have the game info and description
# Things on it: who's left, leaderboard, game feed
# Will have link to stats

@my_app.route('/game/<idd>')
def game(idd):
    idd = int(idd)
    if "user" not in session:
        return redirect(url_for('login'))
    gamee = db.getGameInfo(idd)
    gamee["adminname"] = session["user"]
    managing = idd in db.getGamesID(db.getUserID(session["user"]))
    p, playing = db.getPlaying(db.getUserID(session["user"]))
    play = idd in playing
    return render_template("game.html", game=gamee, admin=managing, playing=play, loggedin=True)


# ==================== FINDGAME =======================
# Adds a user to a game depending on the key inputted
# The layout of this is unclear

@my_app.route('/fndgame')
def fndgame():
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template("search.html", loggedin=True)

@my_app.route("/checkKey", methods=["POST"])
def checkkey():
    if "user" not in session:
        return redirect(url_for('login'))
    key = request.form["key"]
    game = db.checkKey(key)
    if game == "doesn't exist":
        flash("The key you entered is invalid. Please try again.")
        return redirect(url_for("fndgame"))
    else:
        db.joinGame(game, db.getUserID(session["user"]))
        flash("Joined game " + str(game))
        print game
        return redirect(url_for("game", idd=game))

# ==================== PROFILE =======================
# User Profile with info and stats and stuff

@my_app.route('/profile')
def profile():
    if "user" not in session:
        return redirect(url_for('login'))
    username = session['user']
    userID = db.getUserID(username)
    name = db.getName(username)
    games = db.getGames(userID)
    playing, p = db.getPlaying(userID)
    return render_template("profile.html", username=username, userID=userID, name=name, games=games, playing=playing, loggedin=True)




if __name__ == "__main__":
    my_app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    my_app.run()
