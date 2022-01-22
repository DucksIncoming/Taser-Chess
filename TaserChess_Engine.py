import chess
import chess.engine
import pygame

# Import stockfish because it's better than anything I can make
engine = chess.engine.SimpleEngine.popen_uci(r"stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")

board = chess.Board()

# Keep depth the same for both searches to avoid weirdness
# Depth is arbitrary but lower depths are more forgiving to players
searchDepth = 10

referenceScore = 0
newScore = 0

print(board)
while not board.is_game_over():

    info = engine.analyse(board, chess.engine.Limit(depth=searchDepth))
    
    # Get a score for the initial position to compare the new score after a move to
    if (board.turn):
        referenceScore = info["score"].white().score()
        print("White's turn:")
    else:
        referenceScore = info["score"].black().score()
        print("Black's turn:")
  
    moveAttempt = input()
    if ((chess.Move.from_uci(moveAttempt) in board.legal_moves) and (board.color_at(chess.parse_square(moveAttempt[0:2])) == board.turn)):
        board.push(chess.Move.from_uci(moveAttempt))

        # Get the new score of the board and find the difference
        info = engine.analyse(board, chess.engine.Limit(depth=searchDepth))
        
        # Fucky weirdness because stockfish returns EVERYTHING as an object
        if (not board.turn):
            newScore = info["score"].white().score()
        else:
            newScore = info["score"].black().score()
        print(newScore)

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(board)

        print("Old Score: " + str(referenceScore) + "\nNew Score: " + str(newScore))
        try:
            print("Diff: " + str(newScore - referenceScore))
        except:
            # Doesn't return infinity/-infinity so I have to do this fucky shit or edit source code so
            print("Diff: Checkmate/Fail Move")

        # Check how bad the move is. 300 is the threshold, equal to roughly 3 pawns. The value
        # is completely arbitrary, higher threshholds cause tazing less often, lower thresholds
        # cause tazing more often. Keep it above 100/200 or it'll taze with basically every move.
        try:
            if (-(newScore - referenceScore) > 300):
                print("Bad Move\n")
            else:
                print("Tolerable Move\n")
        except:
            print("Checkmate/Fail Move")
    else:
        print("Move is not legal. Please retry.")
    
    if (board.is_game_over()):
        try:
            print(board.winner())
        except:
            print("Draw")

engine.quit()