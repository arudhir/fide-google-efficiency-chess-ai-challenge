# submission/bots/hybrid_bot.py
from Chessnut import Game
import random
from .utils import PIECE_VALUES

def evaluate_move(game, move):
    """Sophisticated move evaluation for non-obvious positions"""
    score = 0
    test_game = Game(game.board.fen)
    test_game.apply_move(move)
    
    # Basic material evaluation
    to_square = Game.xy2i(move[2:4])
    captured_piece = game.board.get_piece(to_square)
    if captured_piece != ' ':
        score += PIECE_VALUES.get(captured_piece.upper(), 0)
    
    # Promotion
    if 'q' in move.lower():
        score += 800
    
    # Center control (e4, d4, e5, d5)
    center_squares = [28, 29, 36, 37]
    if to_square in center_squares:
        score += 30
    
    # Rook on open file
    piece = game.board.get_piece(Game.xy2i(move[0:2]))
    if piece.upper() == 'R':
        file_idx = to_square % 8
        open_file = True
        for rank in range(8):
            if test_game.board.get_piece(rank * 8 + file_idx).upper() == 'P':
                open_file = False
                break
        if open_file:
            score += 50
            
    return score

def chess_bot_hybrid(obs):
    """
    Hybrid chess bot that uses simple priorities first, then falls back to sophisticated evaluation.
    """
    try:
        # Parse the current board state
        game = Game(obs['board'])
        moves = list(game.get_moves())
        
        if not moves:
            return ""
            
        # 1. First priority: Checkmate
        for move in moves[:10]:  # Check first 10 moves for quick mates
            g = Game(obs['board'])
            g.apply_move(move)
            if g.status == Game.CHECKMATE:
                return move
        
        # 2. Second priority: Captures
        captures = []
        for move in moves:
            if game.board.get_piece(Game.xy2i(move[2:4])) != ' ':
                captures.append(move)
        if captures:
            # If there are multiple captures, evaluate them
            if len(captures) > 1:
                capture_scores = [(move, evaluate_move(game, move)) for move in captures]
                return max(capture_scores, key=lambda x: x[1])[0]
            return captures[0]
        
        # 3. Third priority: Queen promotions
        for move in moves:
            if "q" in move.lower():
                return move
        
        # 4. Fourth priority: Evaluate remaining moves
        # Only evaluate top 10 moves to save time
        move_scores = []
        for move in moves:
            score = evaluate_move(game, move)
            move_scores.append((move, score))
        
        # Sort by score and select from top 3
        if move_scores:
            move_scores.sort(key=lambda x: x[1], reverse=True)
            top_moves = move_scores[:3]
            return random.choice([move for move, _ in top_moves])
        
        # 5. Final fallback: Random move
        return random.choice(moves)
        
    except Exception as e:
        # Emergency fallback
        try:
            game = Game(obs['board'])
            moves = list(game.get_moves())
            if moves:
                return random.choice(moves)
            return ""
        except:
            return ""
