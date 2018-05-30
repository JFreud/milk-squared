from flask import Flask, render_template, request, session, redirect, url_for, flash
from os import path, urandom
from utils import db
import json, urllib2, sys, sqlite3

my_app = Flask(__name__)
my_app.secret_key = urandom(64)

DIR = path.dirname(__file__)
#console output will appear in /var/log/apache2/error.log

# ==================== HOME =======================
# If logged in displays home/feed
# If not, redirects to login page

@my_app.route('/')
def root():
    if "user" not in session:
        return redirect(url_for('login'))
    # return render_template("login.html")
    return render_template('index.html')

@my_app.route('/feed')
def feed():
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template("feed.html")

# ==================== CREATE ACCOUNT =======================
@my_app.route('/register', methods=['GET','POST'])
# Account creation (duh)
def register():
    # do db stuff and make account
    #if request.method == "GET":
    return render_template('register.html')
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
        return render_template('login.html')
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
        flash ("Logged out " + username)
        return redirect(url_for('login'))
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
       return render_template("mkgame.html")


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
    joinKey = request.form['joinKey']
    title = request.form['title']
    description = request.form['description']
    if gameMode == "Assassins - Rapid Fire":
        typ = 0
    elif gameMode == "Assassins - Last Man Standing":
        typ = 1
    elif gameMode == "Secret Santa":
        typ = 2
    gameID = db.crGame(adminID, joinKey, gameMode, startDate, endDate, title, description)
    session['game'] = gameID
    session["gameType"] = typ
    return render_template("rules.html", gameType = typ)

@my_app.route('/rule_creation', methods=["POST"])
def create_rules():
    if "user" not in session:
        return redirect(url_for('login'))
    if "game" not in session or "gameType" not in session:
        flash("Please try again.")
        return redirect(url_for("profile"))
    if "maxPeople" in request.form:
        gameMode = session['gameType']
        gameID = session["game"]
        if gameMode == 0 or gameMode == 1:
            maxPeople = int(request.form['maxPeople'])
            safeZones = request.form['safeZones']
            db.crRulesA(session["game"], gameMode, maxPeople, safeZones)
        elif gameMode == 2:
            maxPeople = int(request.form['maxPeople'])
            spending = int(request.form['spending'])
            db.crRulesSS(session["game"], maxPeople, spending)
    else:
        db.deleteGame(session["game"])
    return redirect(url_for('profile'))

# ==================== GAME =======================
# Main game page that will have the game info and description
# Things on it: who's left, leaderboard, game feed
# Will have link to stats


@my_app.route('/game')
def game():
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template("vwgame.html")

# ==================== SEARCH =======================
# Search option for games and users
# The layout of this is unclear

@my_app.route('/search')
def search():
    # DO THE SEARCH
    # DROPDOWN ON SEARCH BAR
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template("search.html")

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
    return render_template("profile.html", username=username, userID=userID, name=name, games=games)




if __name__ == "__main__":
    my_app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    my_app.run()
