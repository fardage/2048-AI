import sys

import numpy

import game

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def evaluate_board(board, newboard):
    layout = heuristic_tile_layout(newboard)
    return layout

def heuristic_tile_layout(board):
    rewardBoard = numpy.array([
        [2 ** 15, 2 ** 14, 2 ** 13, 2 ** 12],
        [2 ** 8, 2 ** 9, 2 ** 10, 2 ** 11],
        [2 ** 7, 2 ** 6, 2 ** 5, 2 ** 4],
        [2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3]
    ])

    value = 0
    for row in range(0, 4):
        for column in range(0, 4):
            value += (board[row][column] * rewardBoard[row][column])
    return value

def board_equals(board, new_board):
    """
    Check if two boards are equal
    """
    return (new_board == board).all()
