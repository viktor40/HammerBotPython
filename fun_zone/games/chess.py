import chess.svg
import chess
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import fun_zone.games.utils as utils

turn_mapping = {"white": chess.WHITE, "black": chess.BLACK}


class ForbiddenChessMove(Exception):
    """Exception raised when using a forbidden chess move.

    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    """

    def __init__(self, message="This is not a valid chess move!"):
        self.message = message
        super().__init__(self.message)


class Chess:
    def __init__(self):
        self.board = None
        self.turn = "white"

    def generate_board(self):
        self.board = chess.Board()
        self.board.turn = chess.WHITE
        utils.gen_png_from_svg(self.board)

    def move_piece(self, move):
        chess_move = chess.Move.from_uci(move)
        if chess_move in self.board.legal_moves:
            self.board.push(chess_move)
            utils.gen_png_from_svg(self.board)
            self.turn = "white" if self.turn == "black" else "black"
            self.board.turn = turn_mapping[self.turn]
        else:
            raise ForbiddenChessMove

    def check_finished(self, arg):
        if arg == "checkmate":
            return self.board.is_checkmate()

        elif arg == "stalemate":
            return self.board.is_stalemate

        elif arg == "draw":
            return self.board.has_insufficient_material(self.board.turn) or self.board.can_claim_draw()
