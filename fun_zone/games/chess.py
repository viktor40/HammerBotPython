import chess.svg
import chess
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

turn_mapping = {"white": chess.WHITE, "black": chess.BLACK}


class ForbiddenChessMove(Warning):
    """Warning raised when using a forbidden chess move.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="This is not a valid chess move!"):
        self.message = message
        super().__init__(self.message)


class Chess:
    """Handles all chess game related actions like generating the board, moving pieces and promoting pawns.

    Attributes:
         board -- a chess.board object containing the current board
         turn -- a string containing the colour of the player who's turn it is
    """

    def __init__(self):
        self.board = None
        self.turn = "white"

    def generate_board(self):
        """Generates the board and converts the .svg file to a .env file"""
        self.board = chess.Board()
        self.board.turn = chess.WHITE
        self.turn = "white"
        self.gen_png_from_svg()

    def move_piece(self, move):
        """
        Move a piece. It checks for illegal moves first. Then it'll move the piece, generate the board
        and change turns. If there is an illegal move a ForbiddenChessMove error will be raised.
        """
        chess_move = chess.Move.from_uci(move)
        if chess_move in self.board.legal_moves:
            self.board.push(chess_move)
            self.gen_png_from_svg()
            self.turn = "white" if self.turn == "black" else "black"
            self.board.turn = turn_mapping[self.turn]

        else:
            raise ForbiddenChessMove()

    def check_finished(self, arg):
        """
        Checks if the conditions are met to end a game.
        :param arg: can be 'checkmate', 'stalemate' or 'draw'. It will return either True or False depending on if the
                    condition was met.
        """
        if arg == "checkmate":
            return self.board.is_checkmate()

        elif arg == "stalemate":
            return self.board.is_stalemate

        elif arg == "draw":
            return self.board.has_insufficient_material(self.board.turn) or self.board.can_claim_draw()

    def promote_pawn(self, move, piece):
        """
        Promote a piece. It checks for illegal moves. Then it'll move the piece and promote it correctly then
        change turns. If there is an illegal move a ForbiddenChessMove error will be raised.

        :param move: the chess move in uci format
        :param piece: the piece in number format. See pieces_mappings in the Games class in games.py
                      It can be found within th chess command in the section for the promote action.
        """
        pseudo_move = chess.Move.from_uci(move)
        chess_move = chess.Move(from_square=pseudo_move.from_square,
                                to_square=pseudo_move.to_square,
                                promotion=piece
                                )

        if chess_move in self.board.legal_moves:
            self.board.push(chess_move)
            self.gen_png_from_svg()
            self.turn = "white" if self.turn == "black" else "black"
            self.board.turn = turn_mapping[self.turn]

        else:
            raise ForbiddenChessMove()

    def gen_png_from_svg(self):
        """
        A function used to first generate a SVG image of the chess board. After this the SVG image
        will be converted to a PNG image.
        """
        board_svg = chess.svg.board(board=self.board)
        output_file = open('board.svg', "w")
        output_file.write(board_svg)
        output_file.close()
        drawing = svg2rlg("board.svg")
        renderPM.drawToFile(drawing, "board.png", fmt="PNG")
