#import chess
#import chess.engine
#import time
#from pyfirmata import Arduino

import pygame
import os
import math

# Constant Variables
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS_CAP = 60
BOARD_ORIGIN = (560, 140)

# Colors
GRAY = (30, 30, 30)

# Customization Variables
boardStyle = "chesscom"
pieceStyle = "standard"

# Boards
boards = {
    "beach": "Assets/Boards/board_beach.png",
    "checkers": "Assets/Boards/board_checkers.png",
    "chesscom": "Assets/Boards/board_chesscom.png",
    "chilly": "Assets/Boards/board_chilly.png",
    "classic": "Assets/Boards/board_classic.png",
    "headache": "Assets/Boards/board_headache.png",
    "hell": "Assets/Boards/board_hell.png",
    "hot": "Assets/Boards/board_hotandsexy.png",
    "minecraft": "Assets/Boards/board_minecraft.png",
    "nonstandard": "Assets/Boards/board_nonstandard.png",
    "soft": "Assets/Boards/board_soft.png",
    "wood": "Assets/Boards/board_wood.png"
}

# Pieces
    # pieces_NAME.get(COLOR_PIECE)
    # ex: pieces_standard.get(w_pawn)
pieces_artistic = {
    "w_pawn": "Assets/Pieces/pieces_artistic/artistic_Wpawn.png",
    "w_knight": "Assets/Pieces/pieces_artistic/artistic_Wknight.png",
    "w_rook": "Assets/Pieces/pieces_artistic/artistic_Wrook.png",
    "w_bishop": "Assets/Pieces/pieces_artistic/artistic_Wbishop.png",
    "w_queen": "Assets/Pieces/pieces_artistic/artistic_Wqueen.png",
    "w_king": "Assets/Pieces/pieces_artistic/artistic_Wking.png",
    "b_pawn": "Assets/Pieces/pieces_artistic/artistic_Bpawn.png",
    "b_knight": "Assets/Pieces/pieces_artistic/artistic_Bknight.png",
    "b_rook": "Assets/Pieces/pieces_artistic/artistic_Brook.png",
    "b_bishop": "Assets/Pieces/pieces_artistic/artistic_Bbishop.png",
    "b_queen": "Assets/Pieces/pieces_artistic/artistic_Bqueen.png",
    "b_king": "Assets/Pieces/pieces_artistic/artistic_Bking.png"
}

pieces_realistic = {
    "w_pawn": "Assets/Pieces/pieces_realistic/realistic_Wpawn.png",
    "w_knight": "Assets/Pieces/pieces_realistic/realistic_Wknight.png",
    "w_rook": "Assets/Pieces/pieces_realistic/realistic_Wrook.png",
    "w_bishop": "Assets/Pieces/pieces_realistic/realistic_Wbishop.png",
    "w_queen": "Assets/Pieces/pieces_realistic/realistic_Wqueen.png",
    "w_king": "Assets/Pieces/pieces_realistic/realistic_Wking.png",
    "b_pawn": "Assets/Pieces/pieces_realistic/realistic_Bpawn.png",
    "b_knight": "Assets/Pieces/pieces_realistic/realistic_Bknight.png",
    "b_rook": "Assets/Pieces/pieces_realistic/realistic_Brook.png",
    "b_bishop": "Assets/Pieces/pieces_realistic/realistic_Bbishop.png",
    "b_queen": "Assets/Pieces/pieces_realistic/realistic_Bqueen.png",
    "b_king": "Assets/Pieces/pieces_realistic/realistic_Bking.png"
}

pieces_silhouuette = {
    "w_pawn": "Assets/Pieces/pieces_silhouette/silhouette_Wpawn.png",
    "w_knight": "Assets/Pieces/pieces_silhouette/silhouette_Wknight.png",
    "w_rook": "Assets/Pieces/pieces_silhouette/silhouette_Wrook.png",
    "w_bishop": "Assets/Pieces/pieces_silhouette/silhouette_Wbishop.png",
    "w_queen": "Assets/Pieces/pieces_silhouette/silhouette_Wqueen.png",
    "w_king": "Assets/Pieces/pieces_silhouette/silhouette_Wking.png",
    "b_pawn": "Assets/Pieces/pieces_silhouette/silhouette_Bpawn.png",
    "b_knight": "Assets/Pieces/pieces_silhouette/silhouette_Bknight.png",
    "b_rook": "Assets/Pieces/pieces_silhouette/silhouette_Brook.png",
    "b_bishop": "Assets/Pieces/pieces_silhouette/silhouette_Bbishop.png",
    "b_queen": "Assets/Pieces/pieces_silhouette/silhouette_Bqueen.png",
    "b_king": "Assets/Pieces/pieces_silhouette/silhouette_Bking.png"
}

pieces_standard = {
    "w_pawn": "Assets/Pieces/pieces_standard/standard_Wpawn.png",
    "w_knight": "Assets/Pieces/pieces_standard/standard_Wknight.png",
    "w_rook": "Assets/Pieces/pieces_standard/standard_Wrook.png",
    "w_bishop": "Assets/Pieces/pieces_standard/standard_Wbishop.png",
    "w_queen": "Assets/Pieces/pieces_standard/standard_Wqueen.png",
    "w_king": "Assets/Pieces/pieces_standard/standard_Wking.png",
    "b_pawn": "Assets/Pieces/pieces_standard/standard_Bpawn.png",
    "b_knight": "Assets/Pieces/pieces_standard/standard_Bknight.png",
    "b_rook": "Assets/Pieces/pieces_standard/standard_Brook.png",
    "b_bishop": "Assets/Pieces/pieces_standard/standard_Bbishop.png",
    "b_queen": "Assets/Pieces/pieces_standard/standard_Bqueen.png",
    "b_king": "Assets/Pieces/pieces_standard/standard_Bking.png"
}

def indexPosition(index : int):
    if (index < 0):
        index = 0
    if (index > 63):
        index = 63
    
    column = math.floor(index / 8)
    row = index % 8

    xPos = (row * 100) + 560
    yPos = (column * 100) + 140

    return (xPos, yPos)

def drawSprite(imagePath : str, position : tuple = (0, 0), scale : tuple = (0, 0)):
    img = pygame.image.load(imagePath)
    if (scale != (0, 0)):
        img = pygame.transform.scale(img, scale)
    
    WIN.blit(img, position)

def initialFenDraw():
    drawSprite(pieces_standard.get("b_rook"), indexPosition(0), (100, 100))
    drawSprite(pieces_standard.get("b_knight"), indexPosition(1), (100, 100))
    drawSprite(pieces_standard.get("b_bishop"), indexPosition(2), (100, 100))
    drawSprite(pieces_standard.get("b_queen"), indexPosition(3), (100, 100))
    drawSprite(pieces_standard.get("b_king"), indexPosition(4), (100, 100))
    drawSprite(pieces_standard.get("b_bishop"), indexPosition(5), (100, 100))
    drawSprite(pieces_standard.get("b_knight"), indexPosition(6), (100, 100))
    drawSprite(pieces_standard.get("b_rook"), indexPosition(7), (100, 100))
    drawSprite(pieces_standard.get("b_pawn"), indexPosition(8), (100, 100))
    drawSprite(pieces_standard.get("b_pawn"), indexPosition(9), (100, 100))
    drawSprite(pieces_standard.get("b_pawn"), indexPosition(10), (100, 100))
    drawSprite(pieces_standard.get("b_pawn"), indexPosition(11), (100, 100))
    drawSprite(pieces_standard.get("b_pawn"), indexPosition(12), (100, 100))
    drawSprite(pieces_standard.get("b_pawn"), indexPosition(13), (100, 100))
    drawSprite(pieces_standard.get("b_pawn"), indexPosition(14), (100, 100))
    drawSprite(pieces_standard.get("b_pawn"), indexPosition(15), (100, 100))

    drawSprite(pieces_standard.get("w_pawn"), indexPosition(48), (100, 100))
    drawSprite(pieces_standard.get("w_pawn"), indexPosition(49), (100, 100))
    drawSprite(pieces_standard.get("w_pawn"), indexPosition(50), (100, 100))
    drawSprite(pieces_standard.get("w_pawn"), indexPosition(51), (100, 100))
    drawSprite(pieces_standard.get("w_pawn"), indexPosition(52), (100, 100))
    drawSprite(pieces_standard.get("w_pawn"), indexPosition(53), (100, 100))    
    drawSprite(pieces_standard.get("w_pawn"), indexPosition(54), (100, 100))
    drawSprite(pieces_standard.get("w_pawn"), indexPosition(55), (100, 100))
    drawSprite(pieces_standard.get("w_rook"), indexPosition(56), (100, 100))
    drawSprite(pieces_standard.get("w_knight"), indexPosition(57), (100, 100))
    drawSprite(pieces_standard.get("w_bishop"), indexPosition(58), (100, 100))
    drawSprite(pieces_standard.get("w_queen"), indexPosition(59), (100, 100))
    drawSprite(pieces_standard.get("w_king"), indexPosition(60), (100, 100))
    drawSprite(pieces_standard.get("w_bishop"), indexPosition(61), (100, 100))
    drawSprite(pieces_standard.get("w_knight"), indexPosition(62), (100, 100))
    drawSprite(pieces_standard.get("w_rook"), indexPosition(63), (100, 100))

def drawWindow():
    WIN.fill(GRAY)
    drawSprite(boards.get(boardStyle), BOARD_ORIGIN)
    initialFenDraw()

    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS_CAP)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
        
        drawWindow()
        

main()