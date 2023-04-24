from othello import *
import copy

# Will explore each possible move equally, we will perform equal amount of playouts for each move
## board is the board state (8x8 grid)
## player is the player's turn
## n is the number of total playouts
def flatMC(board, player, n = 1000):
    moves = get_moves(board, player)
    bestScore = 0
    bestMove = 0
    for m in range(len(moves)):
        sum = 0
        for _ in range(int(n / len(moves))):
            #Copy the current board
            sim_board = copy.deepcopy(board)
            #Make the move
            make_move(sim_board, player, moves[m][0], moves[m][1])
            opponent = 3 - player
            #Perform a Playout and get the result
            r = playout(sim_board, opponent) 
            if player == 2: #playout return score is based on player 1, so if we are player 2 we minus it
                r = -r
            sum = sum + r
        if sum > bestScore:
            bestScore = sum
            bestMove = m
    return moves[bestMove]