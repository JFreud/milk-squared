from random import randint

'''
    players: a list of player ids for a particular game
    returns: a dictionary denoting each player's target
'''
def getTargets( players ):
    targetDict = dict()
    numPlayers = len(players)

    current = 0
    next = 1

    for i in range(numPlayers):
        # get the index of the next target
        next = randint( 0, len(players) )
        # set the current player's target
        targetDict[current] = players[next]
