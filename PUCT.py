from othello import *
from math import sqrt, log
import copy


#Need a neural network for this
#Not working

MaxLegalMoves = 30
Table = {}
def add(board, player):
    nplayouts = [0.0 for x in range (MaxLegalMoves)]
    nwins = [0.0 for x in range (MaxLegalMoves)]
    nprior = [0.0 for x in range (MaxLegalMoves)]
    Table[get_hash(board, player)] = [0, nplayouts, nwins, nprior]
    return look(board, player)

    # print(get_hash(board, player))
def look(board, player):
    return Table.get(get_hash(board, player), None)

def PUCT(board, player):
    if is_terminal(board):
        return get_winner(board)
    t = look(board, player)
    print(t)
    if t != None:
        bestValue = -1000000.0
        best = 0
        moves = get_moves(board, player)
        for i in range(0, len(moves)):
            # t [4] = value from the neural network
            Q = t[4]
            if t[1][i] > 0:
                Q = t[2][i] / t[1][i]
            if player == 2:
                Q = 1 - Q
            # t [3] = policy from the neural network
            val = Q + 0.4 * t[3][i] * sqrt (t[0]) / (1 + t[1][i])
            if val > bestValue:
                bestValue = val
                best = i
        
        make_move(board, player, moves[best][0], moves[best][1])
        player = 3 - player

        res = PUCT(board, player)
        t[0] += 1
        t[1][best] += 1
        t[2][best] += res
        return res
    else:
        t = add(board, player)
        print(len(t))
        return t[4]
    

def BestMovePUCT(board, player, n=100):
    global Table
    Table = {}
    for i in range(n):
        b1 = copy.deepcopy(board)
        res = PUCT(b1, player)
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