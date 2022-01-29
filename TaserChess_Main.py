import chess
import chess.engine
import time
from pyfirmata import Arduino
from TaserChess_Engine import *

import pygame
import pygame.font
import os
import math

pygame.font.init()

# Constant Variables
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS_CAP = 60
BOARD_ORIGIN = (560, 140)
WHITE_PIN = 9
BLACK_PIN = 8
PORT = "COM6"
FONT = pygame.font.Font(None, 150)

try:
    ardBoard = Arduino(PORT)
    print("Ready")
except:
    print("Arduino board not plugged in! (Or not accessible on specified port)")
    time.sleep(5000)
    quit()

charToPiece = {
        "k": "king",
        "q": "queen",
        "r": "rook",
        "b": "bishop",
        "n": "knight",
        "p": "pawn"
    }

# Colors
GRAY = (30, 30, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Backgrounds
backgrounds = {
    True: "Assets/Icons/background_white.png",
    False: "Assets/Icons/background_black.png"
}

# Arrows
arrows = {
    True: "Assets/Icons/whiteturn_arrow.png",
    False: "Assets/Icons/blackturn_arrow.png"
}

# Boards
boards = {
    "Chess.com": "Assets/Boards/board_chesscom.png",
    "Beach": "Assets/Boards/board_beach.png",
    "Checkers": "Assets/Boards/board_checkers.png",
    "Chilly": "Assets/Boards/board_chilly.png",
    "Classic": "Assets/Boards/board_classic.png",
    "Headache": "Assets/Boards/board_headache.png",
    "Hell": "Assets/Boards/board_hell.png",
    "Hot": "Assets/Boards/board_hotandsexy.png",
    "Minecraft": "Assets/Boards/board_minecraft.png",
    "Soft": "Assets/Boards/board_soft.png",
    "Wood": "Assets/Boards/board_wood.png",
    "Void": "Assets/Boards/board_void.png",
    "Non-Standard": "Assets/Boards/board_nonstandard.png"
}

boardCustomizer = {
    1: "Chess.com",
    2: "Checkers",
    3: "Beach",
    4: "Chilly",
    5: "Classic",
    6: "Headache",
    7: "Hell",
    8: "Hot",
    9: "Minecraft",
    10: "Soft",
    11: "Wood",
    12: "Void",
    13: "Non-Standard" 
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

pieces_silhouette = {
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

pieceCustomizer = {
    1: "Standard",
    2: "Silhouette",
    3: "Artistic",
    4: "Realistic"
}

# Customization Variables
boardStyle = boards.get("Chess.com")
boardStyleIndex = 1
pieceStyle = "Standard"
pieceStyleIndex = 1

def indexToSquare(index : int):
    if (index < 0):
        index = 0
    if (index > 63):
        index = 63

    fileList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    rankList = ['1', '2', '3', '4', '5', '6', '7', '8']

    column = 7 - (math.floor(index / 8))
    row = index % 8

    return (fileList[row] + rankList[column])

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

def getMouseSquare(position : tuple):
    column : int = 0
    row : int = 0

    for colCheck in range(8):
        if (position[1] > (colCheck * 100 + BOARD_ORIGIN[1]) and position[1] < (colCheck * 100 + BOARD_ORIGIN[1] + 100)):
            column = colCheck
            break
    
    for rowCheck in range(8):
        if (position[0] > (rowCheck * 100 + BOARD_ORIGIN[0]) and position[0] < (rowCheck * 100 + BOARD_ORIGIN[0] + 100)):
            row = rowCheck
            break
    
    return (column * 8) + row

def customize():
    mousePos = pygame.mouse.get_pos()

    global boardStyleIndex
    global pieceStyleIndex
    global pieceStyle
    global boardStyle

    # Check which button got clicked
    # drawSprite("Assets/Icons/customization.png", ((1920/2 - 400), 10), (800, 106))

    # Board-Left
    if (mousePos[1] > 116):
        if (mousePos[0] > 560 and mousePos[0] < 625):
            boardStyleIndex -= 1
            if (boardStyleIndex == 0):
                boardStyleIndex = 13
        
        # Board-Right
        elif (mousePos[0] > 860 and mousePos[0] < 925):
            boardStyleIndex += 1
            if (boardStyleIndex == 14):
                boardStyleIndex = 1

        # Piece-Left
        elif (mousePos[0] > 1000 and mousePos[0] < 1065):
            pieceStyleIndex -= 1
            if (pieceStyleIndex == 0):
                pieceStyleIndex = 4
        # Piece-Right
        elif (mousePos[0] > 1300 and mousePos[0 < 1365]):
            pieceStyleIndex += 1
            if (pieceStyleIndex == 5):
                pieceStyleIndex = 1
        
        pieceStyle = pieceCustomizer.get(pieceStyleIndex)
        boardStyle = boards.get(boardCustomizer.get(boardStyleIndex))
    

def drawSprite(imagePath : str, position : tuple = (0, 0), scale : tuple = (0, 0)):
    img = pygame.image.load(imagePath)
    if (scale != (0, 0)):
        img = pygame.transform.scale(img, scale)
    
    WIN.blit(img, position)

def drawHeldPiece(pieceSymbol):
    drawWindow()
    pieceSelection = ""
    if (pieceSymbol != ""):
        if (pieceSymbol.isupper()):
            pieceSelection = "w_"
        else:
            pieceSelection = "b_"

        #print(pieceSymbol.lower())

        pieceSelector = pieceSelection + charToPiece.get(pieceSymbol.lower())

        if (pieceStyle == "Standard"):
            piecePath = pieces_standard.get(pieceSelector, "Assets/Pieces/x.png")
        elif (pieceStyle == "Silhouette"):
            piecePath = pieces_silhouette.get(pieceSelector, "Assets/Pieces/x.png")
        elif (pieceStyle == "Artistic"):
            piecePath = pieces_artistic.get(pieceSelector, "Assets/Pieces/x.png")
        else:
            piecePath = pieces_realistic.get(pieceSelector, "Assets/Pieces/x.png")
        
        #print(piecePath)

        img = pygame.image.load(piecePath)
        img = pygame.transform.scale(img, (100, 100))
        WIN.blit(img, ((pygame.mouse.get_pos()[0] - 50), pygame.mouse.get_pos()[1] - 50))
    pygame.display.update()

class Piece():
    _pieceList = []

    def __init__(self, piecePath, indexPos : int):
        self._pieceList.append(self)
        
        self.image = pygame.transform.scale(pygame.image.load(piecePath), (100, 100))
        self.index = indexPos
        self.x = indexPosition(indexPos)[0]
        self.y = indexPosition(indexPos)[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.index = indexPos

        WIN.blit(self.image, (self.x, self.y))

    def drawPiece(self):
        WIN.blit(self.image, (self.x, self.y))

    def collideCheck(self, mouse):
        return self.rect.collidepoint(mouse)

    def killPiece(self):
        self._pieceList.remove(self)

def drawWindow():
    global boardStyle
    
    WIN.fill(GRAY)
    #drawSprite(backgrounds.get(board.turn), (0,0))
    drawSprite(boards.get(boardStyle), BOARD_ORIGIN)
    drawFromFen(board.fen(shredder=True))
    drawUI()
    pygame.display.update()

def drawUI():
    whiteText = FONT.render(str(whiteTazes), True, WHITE)
    blackText = FONT.render(str(blackTazes), True, WHITE)

    drawSprite("Assets/Icons/text_logo.png", (0, 920), (500, 160))
    drawSprite("Assets/Icons/turn_icons.png", ((BOARD_ORIGIN[0] - 54)/2, 400-291 + BOARD_ORIGIN[1]), (108, 582))
    drawSprite(arrows.get(board.turn), ((BOARD_ORIGIN[0] - 55)/2, 400-85 + BOARD_ORIGIN[1]), (110, 170))
    
    drawSprite("Assets/Icons/taser_icons.png", ((BOARD_ORIGIN[0] + 900), BOARD_ORIGIN[1]), (90, 800))
    WIN.blit(whiteText, (BOARD_ORIGIN[0] + 1050, BOARD_ORIGIN[1]))
    WIN.blit(blackText, (BOARD_ORIGIN[0] + 1050, BOARD_ORIGIN[1] + 720))

    drawSprite("Assets/Icons/customization.png", ((1920/2 - 400), 10), (800, 106))

def drawFromFen(fen : str):
    global pieceStyle
    
    for p in Piece._pieceList:
        p.killPiece()

    pieceSelector = ""
    referenceIndex = 0
    
    # Trim down fen for only the useful bits
    # Is there a better way to do this? Almost certainly.
    # Am I gonna do it better? Not a chance
    fen = fen[0:-3]
    fen = fen.replace('/','')
    fen = fen.replace('H','')
    fen = fen.replace('h','')
    fen = fen.replace('A','')        # Sorry if you're like a competent programmer and this causes you physical pain
    fen = fen.replace('a','')
    fen = fen.replace('-','')
    fen = fen.replace(' ','')
    fen = fen[:-1]

    #print(fen)

    for fenChar in fen:
        if (fenChar.isdigit()):
            if (referenceIndex + int(fenChar) < 64):
                referenceIndex += int(fenChar)
            else:
                fen = fen[:-1]
            
        else:
            if (fenChar.isupper()):
                pieceSelector = "w_"
            else:
                pieceSelector = "b_"

            pieceSelector = pieceSelector +  str(charToPiece.get(fenChar.lower()))
            if (type(pieceSelector) != None):
                piecePath = ""

                if (pieceStyle == "Standard"):
                    piecePath = pieces_standard.get(pieceSelector)
                elif (pieceStyle == "Silhouette"):
                    piecePath = pieces_silhouette.get(pieceSelector)
                elif (pieceStyle == "Artistic"):
                    piecePath = pieces_artistic.get(pieceSelector)
                else:
                    piecePath = pieces_realistic.get(pieceSelector)
                
                Piece(piecePath, referenceIndex)
                referenceIndex += 1
    
#pygame.display.update()
def invertIndex(ind : int):
    #i am so fucking mad that i have to make this
    newFile = 7 - math.floor(ind / 8)
    newRank = ind % 8
    #print("Old: " + str(ind))
    #print(("New: " + str((8 * newFile) + newRank)))
    return (8 * newFile) + newRank

blackTazes = 0
whiteTazes = 0

def badMove():
    global whiteTazes
    global blackTazes

    player = not board.turn
    if (player == chess.WHITE):
        whiteTazes += 1
        ardBoard.digital[WHITE_PIN].write(1)
        time.sleep(0.5)

    else:
        blackTazes += 1
        ardBoard.digital[BLACK_PIN].write(1)
        time.sleep(0.5)

def main():
    global pieceStyle
    global boardStyle
    global pieceStyleIndex
    global boardStyleIndex

    pygame.font.init()

    prevMouseState = False
    clock = pygame.time.Clock()
    run = True
    fromSquare = ""
    toSquare = ""
    globalPSymbol = ""
    heldPieceIndex = 0
    heldPieceIcon = ""

    #drawWindow()

    #pygame.display.update()

    pieceStyleIndex = 1
    boardStyleIndex = 1
    pieceStyle = "Standard"
    boardStyle = "Assets/Boards/board_chesscom.png"


    pieceStyle = pieceCustomizer.get(pieceStyleIndex)
    boardStyle = boards.get(boardCustomizer.get(boardStyleIndex))

    while run:
        drawWindow()

        #if (pygame.mouse.get_pressed()[0]):
            #customize()

        pygame.display.set_caption("TaserChess")
        pygame.display.set_icon(pygame.image.load("Assets/Icons/logo.png"))
        clock.tick(FPS_CAP) 
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        if (pygame.mouse.get_pressed()[0] and not prevMouseState): # Gets the initial square you press down on
            mousePos = pygame.mouse.get_pos()

            prevMouseState = True
            for p in Piece._pieceList:
                if (p.collideCheck(mousePos)):
                    try:
                        if (board.turn == chess.WHITE):
                            #print(invertIndex(p.index))
                            globalPSymbol = board.piece_at(invertIndex(p.index)).symbol()
                            fromSquare = indexToSquare(p.index)
                            #print(indexToSquare(getMouseSquare(mousePos)))
                        else:
                            # Holy fucking SHIT I have no fucking idea how this works??? does the board index reverse depending
                            # on who's turn it is????? i spent like four fucking days trying to figure this out this is the dumbest
                            # shit i have seen in my entire life and i am furious
                            # (it is probably my fault but still)
                            #print(invertIndex(p.index))
                            globalPSymbol = board.piece_at(invertIndex(p.index)).symbol()
                            fromSquare = indexToSquare(p.index)
                            #print(indexToSquare(getMouseSquare(mousePos)))
                        heldPieceIcon = globalPSymbol
                        heldPieceIndex = invertIndex(p.index)

                        board.remove_piece_at(heldPieceIndex)
                        drawHeldPiece(globalPSymbol)
                    except:
                        try:
                            drawHeldPiece(globalPSymbol)
                        except:
                            globalPSymbol = ""
        elif (not pygame.mouse.get_pressed()[0] and prevMouseState): # Gets the square you let go of your mouse on
            toSquare = indexToSquare(getMouseSquare(mousePos))
            prevMouseState = False

            if (fromSquare != toSquare):
                moveAttempt = fromSquare + toSquare
                try:
                    if (heldPieceIcon != ""):
                            board.set_piece_at(heldPieceIndex, chess.Piece.from_symbol(heldPieceIcon))
                            heldPieceIcon = ""
                    if (chess.Move.from_uci(moveAttempt) in board.legal_moves):
                        #print(moveAttempt)
                        globalPSymbol = ""
                        engineAnalysis(moveAttempt)
                        #drawWindow()
                    else:
                        globalPSymbol = ""
                        if (heldPieceIcon != ""):
                            board.set_piece_at(heldPieceIndex, chess.Piece.from_symbol(heldPieceIcon))
                            heldPieceIcon = ""
                except:
                    globalPSymbol = ""
                    if (heldPieceIcon != ""):
                        board.set_piece_at(heldPieceIndex, chess.Piece.from_symbol(heldPieceIcon))
                        heldPieceIcon = ""
            else:
                globalPSymbol = ""
                if (heldPieceIcon != ""):
                    board.set_piece_at(heldPieceIndex, chess.Piece.from_symbol(heldPieceIcon))
                    heldPieceIcon = ""
        elif (pygame.mouse.get_pressed()[0]):
            prevMouseState = pygame.mouse.get_pressed()[0]
            mousePos = pygame.mouse.get_pos()
            if (globalPSymbol != ""):
                drawHeldPiece(globalPSymbol)
            #print(getMouseSquare(mousePos))
        else:
            if (globalPSymbol != ""):
                drawHeldPiece(globalPSymbol)
    
    pygame.quit()