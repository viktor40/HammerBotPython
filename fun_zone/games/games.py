import discord
from discord.ext import commands
from fun_zone.games.chess import Chess
from fun_zone.games.hangman import Hangman
import fun_zone.games.game_data as gd

import help_command.help_data as hd


class Games(commands.Cog):
    """Handles all commands that are used for the games.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
        chess_game -- a fun_zone.games.chess.Chess object containing the complete chess game
        hangman -- a fun_zone.games.hangman.Hangman object containing the hangman game
    """

    def __init__(self, bot):
        self.bot = bot
        self.chess_game = Chess()
        self.hangman = Hangman()

    @commands.command(name='chess', help=hd.chess_help, usage=hd.chess_usage, pass_context=True)
    async def chess(self, ctx, action, move=""):
        """
        :param action: The action to be performed. If the action is 'new' a new board and game will start.
                       If the action is 'move' you can move a piece on the board.
                       If the action is 'checkmate', 'stalemate' or 'draw' it will check if the conditions to end the
                       game are met.
        :param move: This parameter contains the move of a piece. Current position first, targeted position second.

        After an action is performed either the board will be sent to discord as a .png or an error message will be
        sent containing what has gone wrong.
        """

        if action == "new":
            self.chess_game.generate_board()
            response = "It's white's turn!"
            await ctx.send(content=response, file=discord.File("board.png"))

        elif action == "move":
            self.chess_game.move_piece(move=move)
            response = "It's {}'s turn!".format(self.chess_game.turn)
            await ctx.send(content=response, file=discord.File("board.png"))

        elif action == "checkmate":
            if self.chess_game.check_finished("checkmate"):
                await ctx.send("The game ended. Checkmate!")
                self.chess_game = Chess()

            else:
                await ctx.send("There isn't a checkmate.")

        elif action == "stalemate":
            if self.chess_game.check_finished("stalemate"):
                await ctx.send("The game ended. stalemate!")
                self.chess_game = Chess()

            else:
                await ctx.send("There isn't a stalemate.")

        elif action == "draw":
            if self.chess_game.check_finished("draw"):
                await ctx.send("The game ended. draw!")
                self.chess_game = Chess()

            else:
                await ctx.send("There isn't a draw.")

        else:
            await ctx.send("Unknown action.")

    @commands.command(name='hangman', help=hd.hangman_help, usage=hd.hangman_usage, pass_context=True)
    async def hangman(self, ctx, action, guess=""):
        """
        :param action: The action to be performed. If the a
        :param guess:

        """
        if action == "start":
            self.hangman = Hangman()
            message = self.hangman.start()
            await ctx.send(message)

        elif action == "stop":
            self.hangman = Hangman()
            response = "The game has stopped, you gave up."
            await ctx.send(response)

        elif action == "guess":
            if not guess or not guess.isalpha():
                await ctx.send("Please choose a valid letter or word to guess.")

            if len(guess) == 1:
                result = self.hangman.guess_letter(guess.upper())
                if self.hangman.tries == 0:
                    result += "\n This was your last try."
                    self.hangman = Hangman()
                    await ctx.send(result)
                else:
                    await ctx.send(result)

            else:
                result = self.hangman.guess_word(guess.upper())
                if self.hangman.tries == 0:
                    result += "\n This was your last try."
                    self.hangman = Hangman()
                    await ctx.send(result)
                else:
                    await ctx.send(result)

        else:
            await ctx.send("Unknown action.")
