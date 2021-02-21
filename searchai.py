import sys

from joblib._multiprocessing_helpers import mp

import game
import heuristicai as ha

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
move_args = [UP, DOWN, LEFT, RIGHT]


# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.


def find_best_move(board, score):
    """
    find the best move for the next turn.
    """

    global UP, DOWN, LEFT, RIGHT
    global move_args

    max_depth = 1
    if score <= 10000:
        max_depth += 0
    elif score <= 20000:
        max_depth += 1
    else:
        max_depth += 2

    pool = mp.Pool(mp.cpu_count())

    result = [pool.apply(score_toplevel_move, args=(i, board, max_depth)) for i in range(len(move_args))]
    best_move = result.index(max(result))

    pool.close()

    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))

    return best_move


def score_toplevel_move(move, board, depth):
    """
    Entry Point to score the first move.
    """

    # Board after the move has been executed
    new_board = execute_move(move, board)

    # Stop recursion
    if board_equals(board, new_board):
        return 0
    if depth == 0:
        return ha.evaluate_board(board, new_board)

    all_possible_boards = get_all_possible_boards(new_board)

    # Compute Moves & Scores
    child_results = []
    count_non_terminal_nodes = 0

    for boardWithNewTile in all_possible_boards:
        result = [score_toplevel_move(i, boardWithNewTile, depth - 1) for i in range(len(move_args))]
        best_score = max(result)
        child_results.append(best_score)
        if best_score != 0:
            count_non_terminal_nodes += 1

    # If terminal
    if count_non_terminal_nodes == 0:
        return 0

    # Calculate final node score
    node_score = 0
    for node in child_results:
        node_score += node / count_non_terminal_nodes

    return node_score


def get_all_possible_boards(board):
    """
    Returns all possible constellation where a 2 has been inserted
    """
    new_boards = []
    for row in range(len(board)):
        for column in range(len(board)):
            tmp = board.copy()
            if board[row][column] == 0:
                tmp[row][column] = 2
                new_boards.append(tmp)
    return new_boards


def execute_move(move, board):
    """
    move and return the grid without a new random tile 
        It won't affect the state of the game in the browser.
    """

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")


def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return (newboard == board).all()
