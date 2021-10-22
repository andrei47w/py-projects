from UI.GUI import Game
from tests.AI_tests import TestAI
from tests.service_tests import TestGame

"""
        CONNECT FOUR

    Connect Four is a two-player connection board game, in which the players 
choose a color and then take turns dropping colored discs into a seven-column, 
six-row vertically suspended grid. The pieces fall straight down, occupying the 
lowest available space within the column. The objective of the game is to be the 
first to form a horizontal, vertical, or diagonal line of four of one's own discs.
Connect Four is a solved game. The first player can always win by playing the 
right moves. 

Use the settings.txt file to change how the game runs!
"""

if __name__ == '__main__':
    game = Game()
    game.start()
