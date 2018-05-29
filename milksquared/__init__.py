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
    return render_template('home.html')

# ==================== CREATE ACCOUNT =======================
@my_app.route('/register', methods=['GET','POST'])
# Account creation (duh)
def register():
    # do db stuff and make account
    if request.method == "GET":
        return render_template('register.html')
    else:
        user = request.form['username']
        passw = request.form['password']
        name = request.form['name']
        if not db.checkUsernames(user):
            db.register(user,passw,name)
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
            flash("invalid username")
            return redirect(url_for('login'))   
        elif not db.verify(user,passw):
            flash("invalid password")
            return redirect(url_for('login'))
        else:
            session['user'] = user
            return redirect(url_for('root'))

# ==================== CREATE GAME =======================
# Page for the user to create the game
# Enters all the game info and stuff
# Form fields: ...

@my_app.route('/crgame')
def mkgame():
   if "user" not in session:
       return redirect(url_for('login'))
   else:
       return render_template("mkgame.html")

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
    return render_template("profile.html")




if __name__ == "__main__":
    my_app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    my_app.run()
