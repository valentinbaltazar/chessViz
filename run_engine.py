"""Module for io with chesss engines"""

import asyncio
import chess
import chess.engine

ENGINE_PATH = './engines/stockfish/stockfish-windows-x86-64-avx2.exe'


async def eval_fen() -> None:
    transport, engine = await chess.engine.popen_uci(ENGINE_PATH)

    board = chess.Board("r1b1q1k1/pp2b1pp/2p5/2npPQ2/3P4/1P2B3/P1PN2PP/R5K1 w - - 1 17")
    info = await engine.analyse(board, chess.engine.Limit(depth=20))
    print(info["score"])

    await engine.quit()


async def get_best_lines():
    # Start the engine
    transport, engine = await chess.engine.popen_uci(ENGINE_PATH)
    
    # Create a chess board (initial position or use any FEN)
    board = chess.Board("r1b1q1k1/pp2b1pp/2p5/2npPQ2/3P4/1P2B3/P1PN2PP/R5K1 w - - 1 17")

    # Analyze the position to get the best lines with evaluations
    info = await engine.analyse(board, chess.engine.Limit(depth=20), multipv=3)  # multipv=3 for top 3 lines
    
    # Print the best lines, evaluations, and moves
    for eval in info:
        # print(eval)
        
        move_sequence = [str(move) for move in eval['pv']]
        evaluation = eval['score']
        print(f"Line: Evaluation: {evaluation} | {' '.join(move_sequence)}")
    
    # Quit the engine
    await engine.quit()



if __name__ == '__main__':
    # asyncio.run(eval_fen())

    asyncio.run(get_best_lines())
