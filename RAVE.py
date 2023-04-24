from othello import *
from math import sqrt, log
import copy

#Does not select good move (bugged)
MaxLegalMoves = 64
MaxCodeLegalMoves = 64
Table = {}

def look(board, player):
    # print_board(board)
    return Table.get(get_hash(board, player), None)


def RAVE(board, player, played):
    if is_terminal(board):
        return get_winner(board)
    t = look(board, player)
    # print(t)
    if t != None:
        bestValue = -1000000.0
        best = 0
        moves = get_moves(board, player)
        if not moves:
            return 0 # or some other value to indicate that there are no legal moves
        bestcode = get_move_code(moves[0])
        for i in range(0, len(moves)):
            val = 1000000.0
            code = get_move_code(moves[i])
            if t[3][code] > 0:
                beta = t[3][code] / (t[1][i] + t[3][code] + 1e-5 * t[1][i] * t[3][code])
                Q = 1
                if t[1][i] > 0:
                    Q = t[2][i] / t[1][i]
                    if player == 2:
                        Q = 1 - Q
                AMAF = t[4][code] / t[3][code]
                if player == 2:
                    AMAF = 1 - AMAF
                val = (1.0 - beta) * Q + beta * AMAF
            if val > bestValue:
                bestValue = val
                best = i
                bestcode = code
        
        make_move(board, player, moves[best][0], moves[best][1])
        player = 3 - player

        played.append(bestcode)
        res = RAVE(board, player, played)
        t[0] += 1
        t[1][best] += 1
        t[2][best] += res
        updateAMAF(t, played, res)
        return res
    else:
        addAMAF(board, player)
        return playoutAMAF(board, player, played)
        

def BestMoveRAVE(board, player, n=30):
    global Table
    Table = {}
    for i in range(n):
        b1 = copy.deepcopy(board)
        res = RAVE(b1, player, played = [])
    t = look(board, player)
    # print(t)
    moves = get_moves(board, player)
    best = moves[0]
    bestValue = t[1][0]
    for i in range (1, len(moves)):
        if (t[1][i] > bestValue):
            bestValue = t[1][i]
            best = moves[i]
    # print(Table)
    # print(best)
    # print(moves)
    # print(best == moves[0])
    return best


def playoutAMAF(board, player, played):
    while(True):
        board = copy.deepcopy(board)
        moves = []
        moves = get_moves(board, player)
        if is_terminal(board):
            return get_winner(board)
        if len(moves) != 0: 
            n = random.randint(0, len(moves) - 1)
            played.append(get_move_code(moves[n]))
            make_move(board, player, moves[n][0], moves[n][1])
        player = 3 - player

def addAMAF(board, player):
    nplayouts = [0.0 for x in range(MaxLegalMoves)]
    nwins = [0.0 for x in range(MaxLegalMoves)]
    nplayoutsAMAF = [0.0 for x in range(MaxCodeLegalMoves)]
    nwinsAMAF = [0.0 for x in range(MaxCodeLegalMoves)]
    Table[get_hash(board, player)] = [0, nplayouts, nwins, nplayoutsAMAF, nwinsAMAF]


def updateAMAF(t, played, res):
    for i in range(len(played)):
        code = played[i]
        seen = False
        for j in range(i):
            if played[j] == code:
                seen = True
        if not seen:
            t[3][code] += 1
            t[4][code] += res