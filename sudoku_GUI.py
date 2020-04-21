import pygame
from sudoku import *
import time

# Color
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 123, 0)


pygame.init()
screen = pygame.display.set_mode((542, 600), 0, 32)
screen.fill(WHITE)
pygame.display.set_caption('Sudoku')


class Board:

    def __init__(self, rows, columns, board, width, height):
        self.rows = rows
        self.columns = columns
        self.cells = [
            [Cell(row, column, board[row][column], width // rows, height // columns) for column in range(columns)] for
            row in range(rows)]
        solve_board(board)
        self.solved_board = board
        self.width = width
        self.height = height
        self.selected = None

    def draw_grid(self):
        margin = self.width // self.rows
        thickness = 1
        for i in range(self.rows + 1):
            if i % 3 == 0:
                thickness = 3
            pygame.draw.line(screen, BLACK, (0, margin * i), (540, margin * i), thickness)
            pygame.draw.line(screen, BLACK, (margin * i, 0), (margin * i, 540), thickness)
            thickness = 1

        for row in self.cells:
            for cell in row:
                cell.draw()

    def copy_board(self):
        return [[self.cells[row][column].value for column in range(self.columns)] for row in range(self.rows)]

    # Place the value into the cell
    def place(self, temp_value, row, column):
        if self.cells[row][column].value == 0:
            # Check to see if the value place is solvable
            if self.solved_board[row][column] == temp_value:
                self.cells[row][column].value = temp_value
                return True
            else:
                self.cells[row][column].temp_value = 0
                return False

    # Move the select outline
    def move_selector(self, x, y):
        if self.selected is not None:
            row, column = self.selected
            self.cells[row][column].selected = False

            row += y
            column += x
            self.cells[row][column].selected = True
            self.selected = (row, column)

    # Set cells selected to True
    def select(self, mouse_pos):
        if self.selected is not None:
            row, column = self.selected
            self.cells[row][column].selected = False

        if mouse_pos[1] < self.height and mouse_pos[0] < self.width:
            row = mouse_pos[1] // (self.width // self.rows)
            column = mouse_pos[0] // (self.height // self.columns)
            self.selected = (row, column)
            self.cells[row][column].selected = True

    # Set cells temp value
    def sketch(self, temp_value):
        if self.selected is not None:
            row, column = self.selected
            self.cells[row][column].temp_value = temp_value

    # Set the selected cell of temp value to 0
    def clear(self):
        if self.selected:
            row, col = self.selected
            if self.cells[row][col].value == 0:
                self.cells[row][col].temp_value = 0

    def is_finished(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].value == 0:
                    return False
        return True

    def solve(self):
        # Transfer all the answer from the solved_board onto the cells
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column].value = self.solved_board[row][column]


class Cell:

    def __init__(self, row, column, value, width, height):
        self.row = row
        self.column = column
        self.value = value
        self.temp_value = 0
        self.selected = False
        self.width = width
        self.height = height

    def draw(self):
        x = self.column * self.width
        y = self.row * self.height

        font = pygame.font.SysFont("comicsans", 40)
        if self.value != 0:
            # Write the value number into the cell
            text = font.render(str(self.value), 1, BLACK)
            screen.blit(text, (
                x + (self.width // 2 - text.get_width() // 2), y + (self.height // 2 - text.get_height() // 2)))

        elif self.temp_value != 0:
            # Sketch the temp number on top left corner
            text = font.render(str(self.temp_value), 1, (128, 128, 128))
            screen.blit(text, (x + 5, y + 5))

        # If this cell is selected then draw a red outline
        if self.selected:
            pygame.draw.rect(screen, RED, (x, y, self.width, self.height), 3)





def new_game():
    global board
    global start_time
    global errors
    global game_over

    new_sudoku_board = get_new_board()
    board = Board(9, 9, new_sudoku_board, 540, 540)
    start_time = time.time()
    errors = 0
    game_over = False


def redraw_board(time, board, errors):
    screen.fill(WHITE)

    font = pygame.font.SysFont("comicsans", 38)
    # Set time
    text = font.render(format_time(time), 1, BLACK)
    screen.blit(text, (400, 555))

    # Draw Strikes
    text = font.render("Errors: {}".format(errors), 1, (255, 0, 0))
    screen.blit(text, (15, 555))

    pygame.draw.rect(screen, ORANGE, (560 // 2 - 60, 553, 110, 40))
    font = pygame.font.SysFont("comicsans", 28)
    text = font.render("New Game".format(errors), 1, BLACK)
    screen.blit(text, (560 // 2 - 55, 565))

    board.draw_grid()


def format_time(seconds):
    secs = seconds % 60
    mins = seconds // 60
    hours = mins // 60

    return "Time: {}:{}".format(str(mins), str(secs))


start_time = time.time()
errors = 0
running = True
game_over = False
board = Board(9, 9, sudoku_board, 540, 540)
while running:
    play_time = round(time.time() - start_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # If the key pressed is between 1 (keycode = 49)  and 9 (keycode = 57), then sketch
            if 49 <= event.key <= 57:
                board.sketch(event.key - 48)

            if event.key == pygame.K_RETURN:
                if board.selected is not None:
                    row, column = board.selected
                    temp_value = board.cells[row][column].temp_value
                    if temp_value != 0:
                        if board.place(temp_value, row, column):
                            if board.is_finished():
                                game_over = True
                                print("Finish")
                        else:
                            errors += 1
            x = 0
            y = 0
            if event.key == pygame.K_UP:
                y = -1
            if event.key == pygame.K_DOWN:
                y = 1
            if event.key == pygame.K_LEFT:
                x = -1
            if event.key == pygame.K_RIGHT:
                x = 1

            board.move_selector(x, y)

            if event.key == pygame.K_SPACE:
                board.solve()
                game_over = True
                redraw_board(play_time, board, errors)

            if event.key == pygame.K_DELETE:
                board.clear()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            # If user clicked new game button
            if 220 <= mouse_position[0] <= 330 and 553 <= mouse_position[1] <= 593:
                game_over = False
                new_game()
            else:
                board.select(mouse_position)

    redraw_board(play_time, board, errors)

    if game_over:
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("GAME OVER".format(errors), 1, RED)
        screen.blit(text, (542 // 2 - 110, 600 // 2 - 100))

    pygame.display.update()

pygame.quit()
