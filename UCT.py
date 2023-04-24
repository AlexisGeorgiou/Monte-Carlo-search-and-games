from othello import *
from math import sqrt, log
import copy

MaxLegalMoves = 30
Table = {}
def add(board, player):
    nplayouts = [0.0 for x in range (MaxLegalMoves)]
    nwins = [0.0 for x in range (MaxLegalMoves)]
    Table[get_hash(board, player)] = [0, nplayouts, nwins]
    # print(get_hash(board, player))
def look(board, player):
    return Table.get(get_hash(board, player), None)

def UCT(board, player):
    if is_terminal(board):
        return get_winner(board)
    t = look(board, player)
    # print(t)
    # print(t)
    # print('========')
    if t != None:
        bestValue = -1000000.0
        best = 0
        moves = get_moves(board, player)
        for i in range(0, len(moves)):
            val = 1000000.0
            if t[1][i] > 0:
                Q = t[2][i] / t[1][i]
                if player == 2:
                    Q = 1 - Q
                val = Q + 0.4 * sqrt(log(t[0]) / t[1][i])
            if val > bestValue:
                bestValue = val
                best = i
        # print(best)
        # print(len(moves))
        moves = get_moves(board, player)
        if not moves:
            return 0 # indicate that there are no legal moves
        # best = 0
        # bestValue = t[1][0]
        # for i in range (1, len(moves)):
        #     if (t[1][i] > bestValue):
        #         bestValue = t[1][i]
        #         best = i
        
        make_move(board, player, moves[best][0], moves[best][1])


        player = 3 - player
        res = UCT(board, player)
        t[0] += 1
        t[1][best] += 1
        # print(type(res))
        # print(type(t[2][best]))
        t[2][best] += res
        return res
    else:
        add(board, player)
        return playout(board, player)

def BestMoveUCT(board, player, n=1000):
    global Table
    Table = {}
    for i in range(n):
        b1 = copy.deepcopy(board)
        res = UCT(b1, player)
    t = look(board, player)
    # print(t)
    moves = get_moves(board, player)
    best = moves[0]
    bestValue = t[1][0]
    for i in range (1, len(moves)):
        if (t[1][i] > bestValue):
            bestValue = t[1][i]
            best = moves[i]
    # print(best)
    # print(moves)
    return best
