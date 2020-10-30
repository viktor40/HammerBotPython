import random
import math
from fun_zone.games.game_data import minesweeper_emotes as emotes


class Minesweeper:
    """
    A class containing the minesweeper game.

    Attributes:
        difficulty -- The difficulty of the game. Options are: easy, medium, hard and extreme.
        rows -- The number of rows in the board.
        columns -- The number of columns in the board.
        difficulty_mapping -- A mapping containing modifiers to change the amount of mines on a given board.
        mines -- The number of mines on the board.
        mine_locations -- The locations of the mines on the board.
        board -- A string representation of the board, ready to be sent to discord.
    """
    def __init__(self, difficulty, rows, columns):
        self.difficulty = difficulty
        self.rows = rows
        self.columns = columns

        self.difficulty_mapping = {'easy': 0.1, 'medium': 0.2, 'hard': 0.3, 'extreme': 0.4}
        self.mines = math.ceil(self.rows * self.columns * self.difficulty_mapping[self.difficulty])

        self.mine_locations = None
        self.board = None

    def generate_board(self):
        """
        This method will generate the complete minesweeper board and calls various helper functions to achieve this.
        First a check is used to ensure the board won't be too big. A board is too big when it exceeds the discord
        character limit.

        Secondly mines are generated.
        Then the location of these mines will be put into a nice string. The string contains emotes representing
        a tile or a bomb. These are put between || so we can hide the tiles and the user can play hangman.
        """

        if self.rows > 20 or self.columns > 20:
            return "Please choose a size where the sides are smaller or equal to 20!"
        elif self.rows * self.columns > 190:
            return "You must choose a size containing no more than 190 tiles."

        self.mine_locations = self.generate_mines()

        self.board = ""
        for i in range(self.columns):
            for j in range(self.rows):
                if (i, j) in self.mine_locations:
                    self.board += "||{}||".format(emotes['bomb'])

                else:
                    mines = self.number_of_mines_in_range(i, j)
                    self.board += "||{}||".format(emotes[mines])

            self.board += '\n'
        return self.board

    def generate_mines(self):
        """
        This method generates a list of mine locations. The locations of the mines are random.
        There is also a check in place to prevent 2 mines on the same location.
        """
        mine_locations = []
        mines = self.mines
        while mines:
            x, y = self.random_mines()
            if (x, y) not in mine_locations:
                mine_locations.append((x, y))
                mines -= 1

        return mine_locations

    def random_mines(self):
        """
        This method will generate a mine on a random position on the board.
        """
        x = random.randint(0, self.columns - 1)
        y = random.randint(0, self.rows - 1)
        return x, y

    def number_of_mines_in_range(self, x, y):
        """
        This method will check how many mines are in range of a given tile.

        :param x: The x position of the tile on the board.
        :param y: The y position of the tile on the board.
        """
        mines = 0
        for i in (1, -1):
            if (x + i, y) in self.mine_locations:
                mines += 1

            if (x, y + i) in self.mine_locations:
                mines += 1

            if (x + i, y + i) in self.mine_locations:
                mines += 1

        if (x - 1, y + 1) in self.mine_locations:
            mines += 1

        if (x + 1, y - 1) in self.mine_locations:
            mines += 1

        return mines
