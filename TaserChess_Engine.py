import chess
import chess.engine
import pygame

# Import stockfish because it's better than anything I can make
engine = chess.engine.SimpleEngine.popen_uci(r"stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")

board = chess.Board()

INFINITY = 9999999

# Keep depth the same for both searches to avoid weirdness
# Depth is arbitrary but lower depths are more forgiving to players
searchDepth = 12

referenceScore = 0
newScore = 0
badMoveMade = False

def engineAnalysis(moveAttempt):
    global badMoveMade
    badMoveMade = False
    
    if not board.is_game_over():
        info = engine.analyse(board, chess.engine.Limit(depth=searchDepth))
    
        # Get a score for the initial position to compare the new score after a move to
        if (board.turn):
            if (str(info["score"].white()) == "#-1"):
                referenceScore = -INFINITY
            elif (str(info["score"].white()) == "#+1"):
                referenceScore = INFINITY
            else:
                referenceScore = info["score"].white().score()

            print("White's turn:")
        else:
            if (str(info["score"].black()) == "#-1"):
                referenceScore = -INFINITY
            elif (str(info["score"].black()) == "#+1"):
                referenceScore = INFINITY
            else:
                referenceScore = info["score"].black().score()
            print("Black's turn:")
    
        if ((chess.Move.from_uci(moveAttempt) in board.legal_moves) and (board.color_at(chess.parse_square(moveAttempt[0:2])) == board.turn)):
            board.push(chess.Move.from_uci(moveAttempt))

            # Get the new score of the board and find the difference
            info = engine.analyse(board, chess.engine.Limit(depth=searchDepth))
            
            # Fucky weirdness because stockfish returns EVERYTHING as an object

            print(info["score"].white())
            print(info["score"].black())

            if (not board.turn):
                if (str(info["score"].white())[:-1] == "#-"):
                    newScore = -INFINITY
                elif (str(info["score"].black())[:-1] == "#+"):
                    newScore= INFINITY
                else:
                    newScore = info["score"].white().score()
            else:
                if (str(info["score"].black())[:-1] == "#-"):
                    newScore = -INFINITY
                elif (str(info["score"].black())[:-1] == "#+"):
                    newScore= INFINITY
                else:
                    newScore = info["score"].black().score()
            #print(newScore)

            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print(board)

            print("Old Score: " + str(referenceScore) + "\nNew Score: " + str(newScore))
            try:
                print("Diff: " + str(newScore - referenceScore))
            except:
                # Doesn't return infinity/-infinity so I have to do this fucky shit or edit source code so
                print("Diff: Checkmate/Fail Move")

            # Check how bad the move is. 400 is the threshold, equal to roughly 4 pawns. The value
            # is completely arbitrary, higher threshold means tazing happens less often, lower threshold means
            # tazing happens more often. I'd keep it arouund where it is. 
            try:
                if (abs(newScore - referenceScore) > 400):
                    print("Bad Move\n")
                    badMoveMade = True
                else:
                    print("Tolerable Move\n")
            except:
                print("Checkmate/Fail Move")
        else:
            print("Move is not legal. Please retry.")
        
        if (board.is_game_over()):
            
            print(board.winner())
    else:
        engine.quit()
        print("Game Over")

def wasBadMove():
    global badMoveMade
    return badMoveMade