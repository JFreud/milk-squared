from flask import Flask, render_template, request, session, redirect, url_for, flash
import json, urllib2, sys
from os import path, urandom
import sqlite3
# from utils import db

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
    return render_template("home.html")

# ==================== CREATE ACCOUNT =======================
# Account creation (duh)
def create_account():
    # do db stuff and make account
    return redirect(url_for('login'))

# ==================== LOGIN =======================
# Login Page

@my_app.route('/login', methods=['GET','POST'])
def login():
    if "user" in session:
        return redirect(url_for('root'))
    return render_template('login.html')

# ==================== AUTHENTICATE =======================
# Verifies login
@my_app.route('/authenticate', methods=['POST'])
def authenticate():
    # if login
    return redirect(url_for('root'))
    #else
    #flash error

# ==================== CREATE GAME =======================
# Page for the user to create the game
# Enters all the game info and stuff
# Form fields: ...

@my_app.route('/create_game')
def create_game():
    return "INSERT CREATE GAME"

# ==================== INIT GAME =======================
# Route that takes response to form and creates the game

@my_app.route('/init_game', methods=['POST'])
def init_game():
    # CREATE GAME AND STUFF
    return redirect(url_for("game"))

# ==================== GAME =======================
# Main game page that will have the game info and description
# Things on it: who's left, leaderboard, game feed
# Will have link to stats

@my_app.route('/game')
def game():
    return "INSERT GAME INFO"

# ==================== SEARCH =======================
# Search option for games and users
# The layout of this is unclear

@my_app.route('/search')
def search():
    # DO THE SEARCH
    # DROPDOWN ON SEARCH BAR
    return redirect(url_for('profile'))

# ==================== PROFILE =======================
# User Profile with info and stats and stuff

@my_app.route('/profile')
def profile():
    return "INSERT USER PROFILE"




if __name__ == "__main__":
    my_app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    my_app.run()
