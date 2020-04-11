"""Tic-tac-toe
Edit the game.txt file with your move and run this file in your terminal: python main.py
"""

import math
import copy

RESULT_X_WINS = 1
RESULT_DRAW = 0
RESULT_O_WINS = -1
PLAYER_X = "x"
PLAYER_O = "o"
WIN_STATES = [
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
]


def get_state():
    "Get current state from game file"
    state = []
    with open("game.txt", "r") as board:
        for row in board:
            state.append([cell for cell in row[:-1]])

    return state


def update_state(state):
    "Update board state"
    with open("game.txt", "w") as board:
        board.truncate()
        for row in state:
            board.write("".join(row) + "\n")

    return state


def player(s):
    "Given a state s, determines the next player"
    moves = "".join(["".join(row) for row in s])
    x_moves = moves.count("x")
    o_moves = moves.count("o")

    if x_moves <= o_moves:
        return PLAYER_X

    return PLAYER_O


def actions(s):
    "Given a state s, determines the possible actions"
    return [
        (x, y) for y, row in enumerate(s) for x, value in enumerate(row) if value == "#"
    ]


def result(s, a):
    "Given a state s and an action a, determines the next state after a is taken"
    if a not in actions(s):
        raise Exception("Invalid action")

    p = player(s)
    next_state = copy.deepcopy(s)
    for y, row in enumerate(s):
        for x, value in enumerate(row):
            if (x, y) == a:
                next_state[y][x] = p

    return next_state


def terminal(s):
    "Given a state s, determines if s is terminal (the game is over)"
    impossible_states = []

    for win_state in WIN_STATES:
        values = "".join([s[y][x] for x, y in win_state])

        if "xxx" in values or "ooo" in values:
            return True

        if "x" in values and "o" in values:
            impossible_states.append(win_state)

    return len(impossible_states) == len(WIN_STATES)


def utility(s):
    "Given a terminal state s, determines the utility (score) of the game"
    for win_state in WIN_STATES:
        values = "".join([s[y][x] for x, y in win_state])

        if "xxx" in values:
            return RESULT_X_WINS

        if "ooo" in values:
            return RESULT_O_WINS

    return RESULT_DRAW


def min_value(s):
    action_taken = None

    if terminal(s):
        return utility(s), action_taken

    value = math.inf

    for action in actions(s):
        _max_value, _ = max_value(result(s, action))

        if _max_value < value:
            value = _max_value
            action_taken = action

    return value, action_taken


def max_value(s):
    action_taken = None

    if terminal(s):
        return utility(s), action_taken

    value = -math.inf

    for action in actions(s):
        _min_value, _ = min_value(result(s, action))

        if _min_value > value:
            value = _min_value
            action_taken = action

    return value, action_taken


if __name__ == "__main__":
    state = get_state()

    if player(state) == "x":
        print("x is playing...")
        _, action = max_value(state)
    else:
        print("o is playing...")
        _, action = min_value(state)

    new_state = update_state(result(state, action))

    for row in new_state:
        print("".join(row))

    if terminal(new_state):
        print("GAME OVER")

        score = utility(new_state)

        if score == RESULT_X_WINS:
            print("Player x wins")
        elif score == RESULT_O_WINS:
            print("Player o wins")
        else:
            print("It's a draw")
