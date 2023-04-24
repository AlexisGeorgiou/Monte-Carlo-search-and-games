# Othello implementation 

# Running this file will start a game against the computer.
# The computer will play a random legal move against you.
import random

# Define the starting game board
board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]



# Define the available moves
def get_moves(board, player):
    if board is None:
        return []
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                if check_move(board, player, i, j):
                    moves.append((i, j))
    return moves

# Check if a move is valid
def check_move(board, player, i, j):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for d in directions:
        x, y = i + d[0], j + d[1]
        if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] == 0 or board[x][y] == player:
            continue
        while board[x][y] != 0:
            x, y = x + d[0], y + d[1]
            if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] == 0:
                break
            if board[x][y] == player:
                return True
    return False



# Make a move
def make_move(board, player, i, j):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    board[i][j] = player
    positions_to_flip = []
    for d in directions:
        x, y = i + d[0], j + d[1]
        if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] == 0 or board[x][y] == player:
            continue
        flips = []
        while board[x][y] != 0:
            flips.append((x, y))
            x, y = x + d[0], y + d[1]
            if x < 0 or x >= 8 or y < 0 or y >= 8:
                flips = []
                break
            if board[x][y] == player:
                positions_to_flip.extend(flips)
                break
    for pos in positions_to_flip:
        board[pos[0]][pos[1]] = player
    # Update the hash value
    hash_value = get_hash(board, player)
    for pos in [(i, j)] + positions_to_flip:
        hash_value ^= HASH_TABLE[pos[0] * BOARD_SIZE + pos[1]][player-1]
    hash_value ^= HASH_TABLE[-1][player]
    return hash_value
    

# Get user input
def get_move(board, moves):
    while True:
        move = input("Enter your move (e.g. 'd3'): ")
        i, j = ord(move[0]) - 97, int(move[1]) - 1
        if (i, j) in moves:
            return i, j
        else:
            print("Invalid move. Try again.")

# Get the final score
def get_score(board):
    score = [0, 0]
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                score[0] += 1
            elif board[i][j] == 2:
                score[1] += 1
    return tuple(score)

# Print the board
def print_board(board):
    print("  1 2 3 4 5 6 7 8")
    print(" +-+-+-+-+-+-+-+-+")
    for i in range(8):
        print(chr(ord('A') + i), end="|")
        for j in range(8):
            if board[i][j] == 1:
                print("X", end="|")
            elif board[i][j] == 2:
                print("O", end="|")
            else:
                print(" ", end="|")
        print("\n +-+-+-+-+-+-+-+-+")

# Creates starting board
def create_board():
    board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
    return board

# Copies board   
def copy_board(board):
    return [row[:] for row in board]

# A playout is a continuation of the game where every move is random for both players
def playout(board, player):
    while True:
        moves = get_moves(board, player)
        if len(moves) == 0:
            # If the player has no valid moves, skip their turn
            player = 3 - player
            moves = get_moves(board, player)
            # If the other player also has no valid moves, end the game
            if len(moves) == 0:
                break
        move = random.choice(moves)
        make_move(board, player, move[0], move[1])
        player = 3 - player
    score = get_score(board)
    return score[0] - score[1]

# Checks if game is terminal
def is_terminal(board):
    if get_moves(board, 1) == [] and get_moves(board, 2) == []:
        return True
    else:
        return False

#Returns next player
def get_next_player(player):

    return 3 - player



# Define the board size for Othello
BOARD_SIZE = 8
# Define the number of possible player values (black, white)
NUM_PLAYERS = 3
# Create a table of random 64-bit integers for each possible position and player combination
HASH_TABLE = [[random.getrandbits(64) for player in range(NUM_PLAYERS)] for position in range(BOARD_SIZE ** 2)]
# Add an additional random 64-bit integer for the player turn
HASH_TABLE.append([random.getrandbits(64) for player in range(NUM_PLAYERS)])

def get_hash(board, player):
    # Compute the hash value of the board state using Zobrist hashing
    hash_value = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece != 0:
                # XOR the random 64-bit integer for this position and player combination
                hash_value ^= HASH_TABLE[row * BOARD_SIZE + col][piece-1]
    # XOR the random 64-bit integer for the player turn
    hash_value ^= HASH_TABLE[-1][player]
    return hash_value

def get_winner(board):
    """
    Returns the player number (1 or 2) that has won the game, or 0 if the game has ended in a tie.
    """
    score = get_score(board)
    if score[0] > score[1]:
        return 1
    elif score[1] > score[0]:
        return 2
    else:
        return 0

def get_move_code(move):
    return move[0]*move[1]

# Game loop
def main():
    player = 1
    while True:
        print_board(board)
        moves = get_moves(board, player)
        if len(moves) == 0:
            # If the player has no valid moves, skip their turn
            player = 3 - player
            moves = get_moves(board, player)
            # If the other player also has no valid moves, end the game
            if len(moves) == 0:
                break
        if player == 1:
            i, j = get_move(board, moves)
        else:
            i, j = random.choice(moves)
        make_move(board, player, i, j)
        player = 3 - player #Changes player
    print_board(board)
    score = get_score(board)
    if score[0] > score[1]:
        print("Player 1 wins!")
    elif score[0] < score[1]:
        print("Player 2 wins!")
    else:
        print("Tie!")


if __name__ == "__main__":
    main()