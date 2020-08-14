import chess.svg
import chess
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def gen_png_from_svg(board):
    boardsvg = chess.svg.board(board=board)
    outputfile = open('board.svg', "w")
    outputfile.write(boardsvg)
    outputfile.close()
    drawing = svg2rlg("board.svg")
    renderPM.drawToFile(drawing, "board.png", fmt="PNG")