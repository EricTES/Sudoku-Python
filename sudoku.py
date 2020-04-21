"""
solving steps
- loop from 1 to 9
- validate number
- if number is validated them call solve() with column + 1
- if non of the numbers work return false

issues
what happens when the index already has a number?
how to we traverse the different rows
"""
import random


def solve_board(board):
    return solve(0, 0, board)


def solve(row, column, board):
    # End of board
    if row == len(board):
        return True
    # End of a row
    if column == len(board[0]):
        return solve(row + 1, 0, board)
    # Skip past pre defined numbers
    if board[row][column] != 0:
        return solve(row, column + 1, board)
    # Trying different numbers
    for i in range(1, 10):
        if validate(row, column, board, i):
            board[row][column] = i
            if solve(row, column + 1, board):
                return True
    # Non of the number worked
    board[row][column] = 0
    return False


def validate(row_check, column_check, board, number_to_validate):
    # check row
    for column in board[row_check]:
        if column == number_to_validate:
            return False
    # check column
    row_length = len(board)
    for row in range(0, row_length):
        if board[row][column_check] == number_to_validate:
            return False

    # check sub-grid
    row_origin = row_check - (row_check % 3)
    column_origin = column_check - (column_check % 3)
    for row in range(row_origin, row_origin + 3):
        for column in range(column_origin, column_origin + 3):
            if board[row][column] == number_to_validate:
                return False

    return True


def get_new_board():
    new_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
    empty_rows = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    random.shuffle(new_board[0])
    print(new_board)

    for i in range(1, 9):
        new_board.append(list(empty_rows))

    solve(0, 0, new_board)

    for row in range(0, 9):
        for column in range(0, 8):
            offset = random.randint(0, 1)
            new_board[row][column + offset] = 0

    return new_board


def print_board(board):
    for row in range(9):
        if row % 3 == 0:
            print('- ' * 19)

        for column in range(9):
            if column % 3 == 0:
                print('|', end='  ')
            print(board[row][column], end='  ')

        print('|')
    print('- ' * 19)


sudoku_board = [[0, 0, 0, 0, 8, 0, 0, 0, 0],
                [8, 0, 9, 0, 7, 1, 0, 2, 0],
                [4, 0, 3, 5, 0, 0, 0, 0, 1],
                [0, 0, 0, 1, 0, 0, 0, 0, 7],
                [0, 0, 2, 0, 3, 4, 0, 8, 0],
                [7, 3, 0, 0, 0, 9, 0, 0, 4],
                [9, 0, 0, 0, 0, 0, 7, 0, 2],
                [0, 0, 8, 2, 0, 5, 0, 9, 0],
                [1, 0, 0, 0, 4, 0, 3, 0, 0]]



#
# print_board(sudoku_board)
# status = solve_board(sudoku_board)
# print(status)
# print_board(sudoku_board)

# new_board()


# [[9, 2, 5, 3, 4, 8, 6, 1, 7]]
# - - - - - - - - - - - - - - - - - - -
# |  9  2  5  |  3  4  8  |  6  1  7  |
# |  1  3  4  |  2  6  7  |  5  8  9  |
# |  6  7  8  |  1  5  9  |  2  3  4  |
# - - - - - - - - - - - - - - - - - - -
# |  2  1  3  |  4  7  5  |  8  9  6  |
# |  4  5  6  |  8  9  1  |  3  7  2  |
# |  7  8  9  |  6  2  3  |  1  4  5  |
# - - - - - - - - - - - - - - - - - - -
# |  3  4  2  |  7  1  6  |  9  5  8  |
# |  5  6  1  |  9  8  4  |  7  2  3  |
# |  8  9  7  |  5  3  2  |  4  6  1  |
# - - - - - - - - - - - - - - - - - - -