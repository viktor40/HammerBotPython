import discord
from discord.ext import commands
from fun_zone.games.chess import Chess
import fun_zone.games.game_data as gd

import help_command.help_data as hd


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chess_game = Chess()

    @commands.command(name='chess', help=hd.chess_help, usage=hd.chess_usage, pass_context=True)
    async def chess(self, ctx, action, move=""):
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
