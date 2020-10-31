import discord
from discord.ext import commands
from fun_zone.games.chess import Chess
from fun_zone.games.hangman import Hangman
from fun_zone.games.minesweeper import Minesweeper
import time

import cogs.help_command.help_data as hd


class Games(commands.Cog):
    """Handles all commands that are used for the games.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
        chess_game -- a fun_zone.games.chess.Chess object containing the complete chess game
        hangman -- a fun_zone.games.hangman.Hangman object containing the hangman game
        minesweeper -- a fun_zone.games.minesweeper.Minesweeper object containing the minesweeper game
    """

    def __init__(self, bot):
        self.bot = bot
        self.chess_game = None
        self.hangman = None
        self.minesweeper = None
        print('> {} Cog Initialised. Took {} s'.format('Games', time.perf_counter() - bot.start_time))
        bot.start_time = time.perf_counter()

    @commands.command(name='chess', help=hd.chess_help, usage=hd.chess_usage, pass_context=True)
    async def chess(self, ctx, action, move='', piece=''):
        """
        :param ctx: a context variable for the command
        :param action: The action to be performed. If the action is 'new' a new board and game will start.
                       If the action is 'move' you can move a piece on the board.
                       If the action is 'promote' you can promote a piece. Specify the move and the piece to promote to.
                       the piece is case insensitive.

                       If the action is 'checkmate', 'stalemate' or 'draw' it will check if the conditions to end the
                       game are met.

        :param move: This parameter contains the move of a piece. Current position first, targeted position second.
        :param piece: This is only used when promoting a pawn

        After an action is performed either the board will be sent to discord as a .png or an error message will be
        sent containing what has gone wrong.
        """

        if action == 'play':
            self.chess_game.generate_board()
            response = "It's white's turn!"
            await ctx.send(content=response, file=discord.File('board.png'))

        elif action == 'move':
            if not move:
                await ctx.send('Please provide a move to play.')

            self.chess_game.move_piece(move=move)
            response = "It's {}'s turn!".format(self.chess_game.turn)
            await ctx.send(content=response, file=discord.File('board.png'))

        elif action == 'promote':
            if not piece:
                await ctx.send('Please provide a piece to promote to.')

            if not move:
                await ctx.send('Please provide a move to play.')

            pieces_mappings = {'knight': 2, 'bishop': 3, 'rook': 4, 'queen': 5}
            if piece.lower() not in pieces_mappings:
                await ctx.send('Please provide a valid piece to promote to.')

            self.chess_game.promote_pawn(move, pieces_mappings[piece.lower()])
            response = "It's {}'s turn!".format(self.chess_game.turn)
            await ctx.send(content=response, file=discord.File('board.png'))

        elif action == 'checkmate':
            if self.chess_game.check_finished('checkmate'):
                await ctx.send('The game ended. Checkmate!')
                self.chess_game = Chess()

            else:
                await ctx.send("There isn't a checkmate.")

        elif action == 'stalemate':
            if self.chess_game.check_finished('stalemate'):
                await ctx.send('The game ended. stalemate!')
                self.chess_game = Chess()

            else:
                await ctx.send("There isn't a stalemate.")

        elif action == 'draw':
            if self.chess_game.check_finished('draw'):
                await ctx.send('The game ended. draw!')
                self.chess_game = Chess()

            else:
                await ctx.send("There isn't a draw.")

        else:
            await ctx.send('Unknown action.')

    @commands.command(name='hangman', help=hd.hangman_help, usage=hd.hangman_usage, pass_context=True)
    async def hangman(self, ctx, action, guess=''):
        """
        :param ctx: a context variable for the command
        :param action: The action to be performed. If the action is start it will initialise the game.
                       If the action is guess, you can guess either a word or a letter.
        :param guess: The word or letter being guessed.

        After an action is performed the bot will send the results. It does this by either sending the initialised
        game or checking if the guess was correct. It also checks for duplicate guesses. If the guess was wrong
        it'll send the hangman character art. It will always send how many tries are left
        """
        if action == 'play':
            self.hangman = Hangman()
            message = self.hangman.start()
            await ctx.send(message)

        elif action == 'stop':
            self.hangman = Hangman()
            response = 'The game has stopped, you gave up.'
            await ctx.send(response)

        elif action == 'guess':
            if not guess or not guess.isalpha():
                await ctx.send('Please choose a valid letter or word to guess.')

            if len(guess) == 1:
                result = self.hangman.guess_letter(guess.upper())
                if self.hangman.tries == 0:
                    result += '\n This was your last try.'
                    self.hangman = Hangman()
                    await ctx.send(result)
                else:
                    await ctx.send(result)

            else:
                result = self.hangman.guess_word(guess.upper())
                if self.hangman.tries == 0:
                    result += '\n This was your last try.'
                    self.hangman = Hangman()
                    await ctx.send(result)
                else:
                    await ctx.send(result)

        else:
            await ctx.send('Unknown action.')

    @commands.command(name='minesweeper', help=hd.minesweeper_help, usage=hd.minesweeper_usage, pass_context=True)
    async def minesweeper(self, ctx, difficulty='medium', size='10x15'):
        """
        A minesweeper game. We initialise a minesweeper class and generate a board. This board gets sent to discord.

        :param ctx: a context variable for the command
        :param difficulty: The difficulty of the game. Options are easy, medium, hard and extreme.
        :param size: The size of the board. Here we must be weary not to create boards bigger than the discord
                     character limit.
        """

        rows, columns = int(size.split('x')[0]), int(size.split('x')[1])
        self.minesweeper = Minesweeper(difficulty, rows, columns)
        board = self.minesweeper.generate_board()
        await ctx.send(board)
