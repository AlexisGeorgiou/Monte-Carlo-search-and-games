import numpy as np
from UCT import *

MaxLegalMoves = 30
MaxCodeLegalMoves = 30

def SequentialHalving(board, player, n=1000):
    Table = {}
    add(board, player)
    moves = get_moves(board, player)
    total = len(moves)
    nplayouts = [0.0 for x in range(MaxCodeLegalMoves)]
    nwins = [0.0 for x in range(MaxCodeLegalMoves)]
    while (len(moves) > 1):
        for move_index, m in enumerate(moves):
            for i in range(int(n // (len(moves) * np.log2(total)))):
                s = copy.deepcopy(board)
                make_move(board, player, moves[move_index][0], moves[move_index][1])
                res = UCT(board, player)
                nplayouts[get_move_code(m)] += 1
                if player == 1:
                    nwins[get_move_code(m)] += res
                else:
                    nwins[get_move_code(m)] += 1.0 - res
        moves = bestHalf(board, player, moves, nwins, nplayouts)
    return moves [0]

def bestHalf(board, player, moves, nwins, nplayouts):
    half = []
    notused = [True for x in range(MaxCodeLegalMoves)]
    for i in range(int(np.ceil(len(moves) / 2))):
        best = -1.0
        bestMove = moves[0]
        for m in moves:
            code = get_move_code(m)
            if notused[code]:
                mu = nwins[code] / nplayouts[code]
                if mu > best:
                    best = mu
                    bestMove = m
        notused[get_move_code(bestMove)] = False
        half.append(bestMove)
    return half

