import random
import math
from fun_zone.games.game_data import minesweeper_emotes as emotes


class Minesweeper:
    def __init__(self):
        self.difficulty = 'medium'
        self.rows = 5
        self.columns = 7
        self.mines = 14
        self.mine_locations = None
        self.board = None

    def generate_board(self, size, difficulty):
        self.difficulty = difficulty
        self.rows, self.columns = int(size.split('x')[0]), int(size.split('x')[1])
        if self.rows > 25 or self.columns > 25:
            return "Please choose a size smaller or equal to 25x25!"

        self.mines = number_of_mines(self.rows, self.columns, self.difficulty)
        self.mine_locations = generate_mines(self.rows, self.columns, self.mines)

        self.board = ""
        print(self.rows, self.columns)
        for i in range(self.columns):
            for j in range(self.rows):
                if (i, j) in self.mine_locations:
                    self.board += "||{}||".format(emotes['bomb'])

                else:
                    mines = mines_in_range(i, j, self.mine_locations)
                    self.board += "||{}||".format(emotes[mines])

            self.board += '\n'
        return self.board


def number_of_mines(rows, columns, difficulty):
    difficulty_mapping = {'easy': 0.1, 'medium': 0.2, 'hard': 0.3, 'extreme': 0.4}
    return math.ceil(rows * columns * difficulty_mapping[difficulty])


def generate_mines(rows, columns, mines):
    mine_locations = []
    while mines:
        x, y = random_mines(rows, columns)
        if (x, y) not in mine_locations:
            mine_locations.append((x, y))
            mines -= 1

    return mine_locations


def random_mines(rows, columns):
    x = random.randint(0, columns - 1)
    y = random.randint(0, rows - 1)
    return x, y


def mines_in_range(x, y, mine_locations):
    mines = 0
    for i in (1, -1):
        if (x + i, y) in mine_locations:
            mines += 1

        if (x, y + i) in mine_locations:
            mines += 1

        if (x + i, y + i) in mine_locations:
            mines += 1

    if (x - 1, y + 1) in mine_locations:
        mines += 1

    if (x + 1, y - 1) in mine_locations:
        mines += 1

    return mines
