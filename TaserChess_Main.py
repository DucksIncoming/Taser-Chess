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

    xPos = (row * 100) + BOARD_ORIGIN[0]
    yPos = (column * 100) + BOARD_ORIGIN[1]

    return (xPos, yPos)

def drawSprite(imagePath : str, position : tuple = (0, 0), scale : tuple = (0, 0)):
    img = pygame.image.load(imagePath)
    if (scale != (0, 0)):
        img = pygame.transform.scale(img, scale)
    
    WIN.blit(img, position)

class Piece():
    _pieceList = []

    def __init__(self, piecePath, indexPos : int):
        self._pieceList.append(self)
        
        self.image = pygame.transform.scale(pygame.image.load(piecePath), (100, 100))
        self.index = indexPos
        self.x = indexPosition(indexPos)[0]
        self.y = indexPosition(indexPos)[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.indexPos = indexPos
        
        WIN.blit(self.image, (self.x, self.y))

    def collideCheck(self, mouse):
        return self.rect.collidepoint(mouse)

def initialFenDraw():
    Piece(pieces_standard.get("b_rook"), 0)
    Piece(pieces_standard.get("b_knight"), 1)
    Piece(pieces_standard.get("b_bishop"), 2)
    Piece(pieces_standard.get("b_queen"), 3)
    Piece(pieces_standard.get("b_king"), 4)
    Piece(pieces_standard.get("b_bishop"), 5)
    Piece(pieces_standard.get("b_knight"), 6)
    Piece(pieces_standard.get("b_rook"), 7)
    Piece(pieces_standard.get("b_pawn"), 8)
    Piece(pieces_standard.get("b_pawn"), 9)
    Piece(pieces_standard.get("b_pawn"), 10)
    Piece(pieces_standard.get("b_pawn"), 11)
    Piece(pieces_standard.get("b_pawn"), 12)
    Piece(pieces_standard.get("b_pawn"), 13)
    Piece(pieces_standard.get("b_pawn"), 14)
    Piece(pieces_standard.get("b_pawn"), 15)

    Piece(pieces_standard.get("w_pawn"), 48)
    Piece(pieces_standard.get("w_pawn"), 49)
    Piece(pieces_standard.get("w_pawn"), 50)
    Piece(pieces_standard.get("w_pawn"), 51)
    Piece(pieces_standard.get("w_pawn"), 52)
    Piece(pieces_standard.get("w_pawn"), 53)    
    Piece(pieces_standard.get("w_pawn"), 54)
    Piece(pieces_standard.get("w_pawn"), 55)
    Piece(pieces_standard.get("w_rook"), 56)
    Piece(pieces_standard.get("w_knight"), 57)
    Piece(pieces_standard.get("w_bishop"), 58)
    Piece(pieces_standard.get("w_queen"), 59)
    Piece(pieces_standard.get("w_king"), 60)
    Piece(pieces_standard.get("w_bishop"), 61)
    Piece(pieces_standard.get("w_knight"), 62)
    Piece(pieces_standard.get("w_rook"), 63)

def drawWindow():
    WIN.fill(GRAY)
    drawSprite(boards.get(boardStyle), BOARD_ORIGIN)
    initialFenDraw()

    pygame.display.update()

def main():
    prevMouseState = False
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS_CAP)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if (pygame.mouse.get_pressed()[0]):
                mousePos = pygame.mouse.get_pos()

                if (not prevMouseState):
                    
                    for p in Piece._pieceList:
                        if (p.collideCheck(mousePos)):
                            print(p.indexPos)
                        
        prevMouseState = pygame.mouse.get_pressed()[0]
        drawWindow()