from othello import *
from random_move import *
from flatMC import *
from UCB import *
from UCT import *
from RAVE import *
from SequentialHalving import *
from PUCT import *
import pandas as pd


# Define a function to run a game with the random_move method
def run_comparison(win_statistics, method1, method2):
    board = create_board()
    player = 1
    while True:
        moves = get_moves(board, player)
        if len(moves) == 0:
            # If the player has no valid moves, skip their turn
            player = 3 - player
            moves = get_moves(board, player)
            # If the other player also has no valid moves, end the game
            if len(moves) == 0:
                break
        if player == 1: #Player 1
            move = method1(board, player)
        else: #Player 2
            move = method2(board, player)
            # move = get_m\\\\\\\\\ove(board, player)
        if check_move(board, player, move[0], move[1]):
            make_move(board, player, move[0], move[1])
            player = 3 - player
    score = get_score(board)
    if score[0] > score[1]:
        #Black won
        win_statistics[0] += 1
    elif score[0] < score[1]:
        #White won
        win_statistics[1] += 1
    else:
        #Tie
        win_statistics[2] += 1


## ROUND_ROBIN tournament, given the list of methods we get a result table
# the result table will contain the win count of the row method against the column method

# Define the list of methods to compare
methods = [random_move, flatMC, UCB, BestMoveUCT, SequentialHalving]
num_games = 10

# Define the table to hold the win counts for each matchup
table = pd.DataFrame(index=[m.__name__ for m in methods], columns=[m.__name__ for m in methods])

# Run comparisons between every pair of methods and add the win counts to the table
# Methods play half games with Black and half with White
total_matchups = 0
for i, method1 in enumerate(methods):
    for j, method2 in enumerate(methods):
        if i < j: #Calculate only the top triangle of the matrix
            #Method1 (First turn) vs Method2 (Second turn)
            win_statistics = [0, 0, 0]
            for k in range(int(num_games/2)):
                run_comparison(win_statistics, method1, method2)
            table.iloc[i,j] = [win_statistics[0], win_statistics[2]]
            #Method1 (Second turn) vs Method2 (First turn)
            win_statistics = [0, 0, 0]
            for k in range(int(num_games/2)):
                run_comparison(win_statistics, method2, method1)
            table.iloc[i,j][0] += win_statistics[1]
            table.iloc[i,j][1] += win_statistics[2]

            #Mirror the results on the bottom triangle of the matrix
            table.iloc[j,i] = [num_games - table.iloc[i,j][0],table.iloc[i,j][1]]
            
            #Logging each matchup
            total_matchups += 1
            print("=====================================================")
            print("MATCH-UP:", str(total_matchups))
            print('Player 1:', method1.__name__, 'vs Player 2:', method2.__name__)
            print(f"Player 1 wins: {table.iloc[i,j][0]}, Ties: {table.iloc[i,j][1]}, Number of Games: {num_games}")

# Table contains win count of method and number of draws
print(table)
table.to_csv('results.csv')