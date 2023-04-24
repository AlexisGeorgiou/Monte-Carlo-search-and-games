from othello import *
from math import sqrt, log
import copy

#We will choose the first move before each playout depending on UCB formula
#This help us to expand on specific branches of the tree and explore where it seems worthy comparing to a flat approach.

## board is the board state (8x8 grid)
## player is the player's turn
## n is the number of total playouts
def UCB(board, player, n = 1000):
    moves = get_moves(board, player)
    sumScores = [0.0 for _ in range(len(moves))]
    nbVisits = [0 for _ in range(len(moves))]
    for i in range(n):
        bestScore = 0
        bestMove = 0
        for m in range(len(moves)):
            score = 1000000
            if nbVisits[m] > 0:
                score = sumScores[m] / nbVisits[m] + 0.4 * sqrt(log(i) / nbVisits[m])
            if score > bestScore:
                bestScore = score
                bestMove = m
        sim_board = copy.deepcopy(board)
        make_move(sim_board, player, moves[bestMove][0], moves[bestMove][1])
        opponent = 3 - player
        r = playout(sim_board, opponent)
        if player == 2: #playout return score is based on player 1, so if we are player 2 we minus it
            r = -r
        sumScores[bestMove] += r
        nbVisits[bestMove] += 1
    bestScore = 0
    bestMove = 0
    for m in range(len(moves)):
        score = nbVisits[m]
        if score > bestScore:
            bestScore = score
            bestMove = m
    return moves[bestMove]