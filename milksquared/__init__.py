from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from os import path, urandom, mkdir, rename
from utils import db, gameutils
import random
import json, urllib2, sys, sqlite3
from datetime import date, datetime

my_app = Flask(__name__)
my_app.secret_key = 'i dont have a secret key'

DIR = path.dirname(__file__)
#console output will appear in /var/log/apache2/error.log

#file uploading and such
PFP_FOLDER = path.abspath(path.join(path.dirname(__file__), "static/pfps"))
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

if not path.isdir(PFP_FOLDER):
    mkdir(PFP_FOLDER)

my_app.config['UPLOAD_FOLDER'] = PFP_FOLDER
my_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
       return redirect(url_for('root'))
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
       return redirect(url_for('root'))
    username = session['user']
    gameMode = request.form['gameMode']
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    if startDate > endDate:
        flash("Start date must be before end date.")
        return redirect(url_for("mkgame"))
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
        return redirect(url_for('root'))
    if "game" not in session or "gameType" not in session:
        flash("Please try making your game again.")
        return redirect(url_for("profile"))
    if "maxPeople" in request.form:
        gameMode = session['gameType']
        gameID = session["game"]
        maxPeople = int(request.form['maxPeople'])
        if maxPeople < 3:
            flash("The maximum number of people has to be greater than 2.")
            return render_template("rules.html", gameType = gameMode, loggedin=True)
        safeZones = request.form['safeZones']
        db.crRules(session["game"], gameMode, maxPeople, safeZones)
    else:
        db.deleteGame(session["game"])
    session.pop("game")
    session.pop("gameType")
    return redirect(url_for('profile'))

# ==================== GAME =======================
# Main game page that will have the game info and description
# Things on it: who's left, leaderboard, game feed
# Will have link to stats

@my_app.route('/game/<idd>')
def game(idd):
    idd = int(idd)
    if "user" not in session:
        return redirect(url_for('root'))
    if db.getMaxPlayers(idd) == -1:
        flash("Game is invalid.")
        return redirect(url_for("profile"))
    gamee = db.getGameInfo(idd)
    gamee["adminname"] = db.getUsername(gamee["managerID"])
    gamee["targetID"] = db.getTarget(db.getUserID(session["user"]), idd, True)
    playerIDs, players = db.getPlayers(idd)
    gamee["players"] = zip(playerIDs, players)
    print gamee["players"]
    if gamee["targetID"] >= 0:
        gamee["targetname"] = db.getName(db.getUsername(gamee["targetID"]))
    if gamee["type"] == 0:
        gamee["type"] = "Assassins - Rapid Fire"
    else:
        gamee["type"] = "Assassins - Last Man Standing"
    managing = idd in db.getGamesID(db.getUserID(session["user"]))
    p, playing = db.getPlaying(db.getUserID(session["user"]))
    play = idd in playing
    return render_template("game.html", game=gamee, admin=managing, playing=play, loggedin=True)

@my_app.route('/startgame', methods=["POST"])
def startgame():
    if "user" not in session:
        return redirect(url_for('root'))
    gameID = int(request.form["gameID"])
    numPlayers, n = db.getPlayers(gameID)
    if len(numPlayers) < 3:
        flash("Not enough people have joined the game.")
        return redirect(url_for("game", idd = gameID))
    gameutils.assign_targets(gameID)
    db.startgame(gameID)
    flash("Game has started.")
    return redirect(url_for("game", idd = gameID))

@my_app.route('/submit_kill/<idd>', methods = ['POST'])
def submit_kill(idd):
    idd = int(idd)
    if "user" not in session:
        return redirect(url_for('root'))
    typ = request.form["timefordeath"]
    if typ == "kill":
        userID = db.getUserID(session["user"])
        targetID = db.getTarget(userID, idd, True)
    else:
        targetID = db.getUserID(session["user"])
        userID = db.getTarget(targetID, idd, False)
    current = datetime.now()
    date = str(current.year) + "-" + str(current.month) + "-" + str(current.day)
    time = str(current.hour) + ":" + str(current.minute) + ":" + str(current.second)
    confirmed = db.killTarget(userID, targetID, idd, time, date)
    if confirmed:
        flash("Kill was confirmed.")
    elif typ == "kill":
        flash("Kill was submitted; please wait for your target to confirm your kill.")
    else:
        flash("Kill was submitted; please wait for your killer to confirm your death.")
    return redirect(url_for("game", idd=idd))

# ==================== FINDGAME =======================
# Adds a user to a game depending on the key inputted
# The layout of this is unclear

@my_app.route('/fndgame')
def fndgame():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("search.html", loggedin=True)

@my_app.route("/checkKey", methods=["POST"])
def checkkey():
    if "user" not in session:
        return redirect(url_for('root'))
    key = request.form["key"]
    game = db.checkKey(key)
    if game == "doesn't exist":
        flash("The key you entered is invalid. Please try again.")
        return redirect(url_for("fndgame"))
    elif game not in db.getGamesID(db.getUserID(session["user"])):
        if len(db.getPlayers(game)) == db.getMaxPlayers(game):
            flash("The game you're trying to join already has its max number of players.")
            return redirect(url_for("game", idd=game))
        db.joinGame(game, db.getUserID(session["user"]))
        flash("Joined game " + str(game))
        return redirect(url_for("game", idd=game))
    flash("You can't join a game you're managing.")
    return redirect(url_for("fndgame"))

# ==================== PROFILE =======================
# User Profile with info and stats and stuff

@my_app.route('/profile')
def profile():
    if "user" not in session:
        return redirect(url_for('root'))
    username = session['user']
    userID = db.getUserID(username)
    name = db.getName(username)
    games = db.getGames(userID)
    gameIDs = db.getGamesID(userID)
    playing, p = db.getPlaying(userID)
    extension = db.getExtension(userID)
    return render_template("profile.html", username=username, userID=userID, name=name, games=zip(games,gameIDs), playing=zip(playing, p), extension=extension, is_own=True, loggedin=True)

@my_app.route('/profile/<idd>')
def profileWithID(idd):
    if "user" not in session:
        return redirect(url_for("root"))
    idd = int(idd)
    person = idd == db.getUserID(session["user"])
    if person:
        return redirect(url_for("profile"))
    username = db.getUsername(idd)
    name = db.getName(username)
    games = db.getGames(idd)
    gameIDs = db.getGamesID(idd)
    playing, p = db.getPlaying(idd)
    extension = db.getExtension(idd)
    return render_template("profile.html", username=username, userID=idd, name=name, games=zip(games, gameIDs), playing=zip(playing, p), extension=extension, is_own=False, loggedin=True)

@my_app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for(profile))
    file = request.files['file']
    print(file)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        userID = db.getUserID(session["user"])
        newname = str(userID)
        file.save(path.join(my_app.config['UPLOAD_FOLDER'], filename))
        extension = filename.split(".")
        extension = str(extension[1])
        source = PFP_FOLDER + "/" + filename
        destination = PFP_FOLDER + "/" + newname + "." + extension
        rename(source,destination)
        db.setExtension(userID, extension)
        flash("Profile picture updated.")
        return redirect(url_for('profile'))
    else:
        flash("File incompatible.")
        return redirect(url_for('profile'))


@my_app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(my_app.config['UPLOAD_FOLDER'], filename)






if __name__ == "__main__":
    my_app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    my_app.run()
