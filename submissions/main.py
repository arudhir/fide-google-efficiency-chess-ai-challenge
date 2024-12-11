import chess
import chess.engine
import random
from memory_profiler import profile

@profile
def chess_bot(fen):
    """
    Improved chess bot that prioritizes:
    1. Checkmate
    2. Captures
    3. Queen promotion
    4. Piece Safety
    5. Random move if no other criteria are met.

    Args:
        fen: A string representing the current board state in FEN format.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4").
    """
    board = chess.Board(fen)

    # 1. Check for Checkmate (Highest Priority)
    checkmate_move = get_checkmate_move(board)
    if checkmate_move:
        return checkmate_move

    # 2. Capture opponent pieces
    capture_move = get_capture_move(board)
    if capture_move:
        return capture_move

    # 3. Queen promotion
    queen_promotion_move = get_queen_promotion_move(board)
    if queen_promotion_move:
        return queen_promotion_move

    # 4. Piece Safety
    safe_move = get_safe_move(board)
    if safe_move:
        return safe_move

    # 5. Random move if no other criteria met
    return random.choice(list(board.legal_moves)).uci()

def get_checkmate_move(board):
    for move in board.legal_moves:
        board.push(move)
        if board.is_checkmate():
            board.pop()
            return move.uci()
        board.pop()
    return None

def get_capture_move(board):
    for move in board.legal_moves:
        if board.is_capture(move):
            return move.uci()
    return None

def get_queen_promotion_move(board):
    for move in board.legal_moves:
        if board.is_queenside_castling(move) or board.is_kingside_castling(move):
            continue
        if move.promotion == chess.QUEEN:
            return move.uci()
    return None

def get_safe_move(board):
    safe_moves = []
    for move in board.legal_moves:
        board.push(move)
        if not board.is_check():
            safe_moves.append(move.uci())
        board.pop()
    if safe_moves:
        return random.choice(safe_moves)
    return None

if __name__ == "__main__":
    # Example board state in FEN format
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    # Run the chess bot and print the chosen move
    move = chess_bot(fen)
    print(f"Chosen move: {move}")
