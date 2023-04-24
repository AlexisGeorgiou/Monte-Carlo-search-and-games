from othello import *
import random

# Define a random_move function that randomly selects a move from the available moves
def random_move(board, player):
    return random.choice(get_moves(board, player))
