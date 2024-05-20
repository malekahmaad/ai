"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0
    for i in board:
        for j in i:
            if j == O:
                count_O += 1
            elif j == X:
                count_X += 1

    if count_X == count_O:
        return  X
    elif count_X > count_O:
        return O
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                moves.add((i, j))

    return moves
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] > 2 or action[1] > 2 or action[0] < 0 or action[1] < 0:
        raise NameError("unavailable move")

    if board[action[0]][action[1]] != EMPTY:
        raise NameError("unavailable move")

    newBoard = copy.deepcopy(board)

    if player(newBoard) == O:
        newBoard[action[0]][action[1]] = O

    elif player(newBoard) == X:
        newBoard[action[0]][action[1]] = X

    return newBoard
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] == X:
        return X

    elif board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] == O:
        return O

    if board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] == X:
        return X

    elif board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] == O:
        return O

    for i in range(len(board)):
        if board[i][0] == board[i][1] and board[i][0] == board[i][2] and board[i][0] == X:
            return X

        elif board[i][0] == board[i][1] and board[i][0] == board[i][2] and board[i][0] == O:
             return O

    for j in range(3):
        if board[0][j] == board[1][j] and board[0][j] == board[2][j] and board[0][j] == X:
            return X

        elif board[0][j] == board[1][j] and board[0][j] == board[2][j] and board[0][j] == O:
             return O

    return None
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None:
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False

    return True

    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1

    elif winner(board) == O:
        return -1

    return 0
    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None

    action = (-1, -1)

    if player(board) == X:
        action = max_value(board)

    elif player(board) == O:
        action = min_value(board)

    return action[1]
    #raise NotImplementedError


def max_value(board):
    if terminal(board) == True:
        return None

    returned_value = [-2, ()]
    moves = actions(board)
    for move in moves:
        newBoard = result(board, move)
        returned = min_value(newBoard)
        if returned == None:
            if winner(newBoard) == X:
                return  [1, move]

            elif winner(newBoard) == X:
                return  [-1, move]
            else:
                return [0, move]

        else:
            if returned_value[0] < returned[0]:
                returned_value[0] = returned[0]
                returned_value[1] = move

    return returned_value

def min_value(board):
    if terminal(board) == True:
        return None

    returned_value = [2, ()]
    moves = actions(board)
    for move in moves:
        newBoard = result(board, move)
        returned = max_value(newBoard)
        if returned == None:
            if winner(newBoard) == X:
                return  [1, move]

            elif winner(newBoard) == O:
                return  [-1, move]

            else:
                return [0, move]

        else:
            if returned_value[0] > returned[0]:
                returned_value[0] = returned[0]
                returned_value[1] = move

    return returned_value
