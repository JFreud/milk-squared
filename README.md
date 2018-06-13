# milksquared
### by milksquared
#### Tiffany Chen, Jerome Freudenberg, Jake Goldman, Augie Murphy
[Play it here](http://milksquared.space/)


### Description
Our website is intended as a resource for groups of people (or individuals looking for a group) to come together and play assassins. The site offers both versions (rapid fire and last man standing) with customizable options. Users create an account and are able to join games using a randomly generated key procured from the person running the game, as well as start a game of their own. The website manages these games for the people playing, including matching people with random targets and keeping track of associated data like kills and players left. The site also tracks user activities as well as the progress of a game and will statistics and graphs based on this data. This means users can look up a game and see stats about it like who has the most kills and can look up user profiles to see their match history and game averages. Ultimately, the site is a great place to have fun with your peers without the additional hassle of having to manage the games yourself.

## Video Link
<insert later>

## Usage Instructions
0. Go to the url above or the one hosted on the stuycs website
1. Create an account using register
2. Add a profile picture so people can recognize you
3. Create or join a game.
4. Have fun!

## Dependencies (if you want to run on localhost)
* `from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory`
  * requires `pip install flask`
* [`python2.7`](https://www.python.org/download/releases/2.7/)
* `import json, sys, os, sqlite3, datetime`
  * should be included with python

## Bugs and Issues
- when you update stuff for the game as an admin and you update only maxNumber with the number being less than 3, the code will flash “must have at least 3 players” and “game settings have been changed” even though no settings would’ve been changed
- similar problem with changing account settings but with passwords
- theres no winner mechanism for rapid fire. if one person kills everybody else playing that day it will announce him or her as winner and end the game despite it not actually having ended.
- can't have too many people playing because of concurrency issues with sqlite.
- svg graphs don't work on safari, we get a typeerror because getElementById can't find the svg. (It works on Chrome and Firefox)
 - this is probably because the script is defined at the top but the function isn't called till later
- no way for an admin to handle a discrepancy

## File Structure
```
docs/
  | DESIGN.pdf
  | DEVLOG.txt
  | log.sh
milksquared/
  data/
    | database.db
  static/
    pfps/
      | default.jpg
    | stuff.css
    | stuff.js
    | txt.txt
  templates/
    | base.html
    | game.html
    | home.html
    | index.html
    | login.html
    | mkgame.html
    | profile.html
    | register.html
    | rules.html
    | search.html
  utils/
    | db.py
    | gameutils.py
  | __init__.py
.gitignore
milksquared.conf
milksquared.wsgi
README.md
```
