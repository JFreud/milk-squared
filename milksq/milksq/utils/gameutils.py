from random import randint
from db import *


'''
    This is a helper function for generating targets at the start of a game.

    args:
        players: a list of player ids for a particular game (should be ints, probably won't matter)
    returns: a dictionary denoting each player's target
'''
def get_targets( players ):
    targetDict = dict()

    # value of the first player for whom we're assigning a target
    first = players.pop( randint(0, len(players) - 1) )

    # set the current player equal to the first player to start
    current = first

    # print 'BEFORE LOOP:\nfirst:%d\ncurrent:%d\nremaining players:%s\n' % (first, current, players)
    while len(players) != 0:
        # get the next player (target for the previous player)
        next = players.pop( randint( 0, len(players) - 1) )

        # set the current player's target
        targetDict[current] = next

        # set the current player to be equal to the previous target
        current = next
        # print 'LOOP PASS FINISHED:\ncurrent:%d\nremaining players:%s\n' % (current, players)

    # set the last player's target to the first player
    targetDict[current] = first

    return targetDict


'''
    This is a function for assigning targets at the start of the game. It will
    get a list of players, generate a dictionary of targets based on that list,
    and assign those targets in the database.

    args:
        gameID: the id of the game for which targets should be assigned
'''
def assign_targets( gameID ):
    pass


# TESTING STUFF
if __name__ == '__main__':
    print 'TESTING get_targets( players ):'
    players = [1, 2, 3, 4, 5]
    print getTargets(players)
