from Chessnut import Game
import random

PIECE_VALUES = {
    'P': 100,   # Pawn
    'N': 320,   # Knight
    'B': 330,   # Bishop
    'R': 500,   # Rook
    'Q': 900,   # Queen
    'K': 20000  # King
}

def evaluate_capture(game, move):
    """Evaluate capture moves by material difference"""
    captured_piece = game.board.get_piece(Game.xy2i(move[2:4]))
    capturing_piece = game.board.get_piece(Game.xy2i(move[0:2]))
    
    captured_value = PIECE_VALUES.get(captured_piece.upper(), 0)
    capturing_value = PIECE_VALUES.get(capturing_piece.upper(), 0)
    
    return captured_value - capturing_value

def chess_bot(obs):
    """
    Chess bot that combines simple priorities with basic positional understanding.
    """
    try:
        game = Game(obs['board'])
        moves = list(game.get_moves())

        if not moves:
            return ""

        # 1. Immediate checkmate
        for move in moves[:10]:
            g = Game(obs['board'])
            g.apply_move(move)
            if g.status == Game.CHECKMATE:
                return move

        # 2. Captures (now with evaluation)
        captures = []
        for move in moves:
            if game.board.get_piece(Game.xy2i(move[2:4])) != ' ':
                captures.append(move)
        
        if captures:
            # Sort captures by material gain
            captures.sort(key=lambda m: evaluate_capture(game, m), reverse=True)
            return captures[0]

        # 3. Queen promotions
        for move in moves:
            if "q" in move.lower():
                return move

        # 4. Simple positional play
        center_squares = [Game.xy2i(sq) for sq in ['e4', 'd4', 'e5', 'd5']]
        for move in moves:
            to_square = Game.xy2i(move[2:4])
            # Prioritize center control in opening/middlegame
            if to_square in center_squares:
                return move
            
            # Look for rook moves to open files
            piece = game.board.get_piece(Game.xy2i(move[0:2]))
            if piece.upper() == 'R':
                file_idx = to_square % 8
                open_file = True
                for rank in range(8):
                    if game.board.get_piece(rank * 8 + file_idx).upper() == 'P':
                        open_file = False
                        break
                if open_file:
                    return move

        # 5. Random move with slight preference for knights and bishops early
        early_moves = [m for m in moves if game.board.get_piece(Game.xy2i(m[0:2])).upper() in ['N', 'B']]
        return random.choice(early_moves) if early_moves else random.choice(moves)

    except Exception as e:
        # Emergency fallback
        try:
            game = Game(obs['board'])
            return random.choice(list(game.get_moves()))
        except:
            return ""

def chess_bot_basic(obs):
    """
    Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

    Args:
        obs: A dictionary with a 'board' key containing the FEN string of the current board state.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    try:
        # 0. Parse the current board state and generate legal moves using Chessnut library
        game = Game(obs['board'])  # Changed from obs.board to obs['board']
        moves = list(game.get_moves())

        if not moves:  # No legal moves
            return ""

        # 1. Check a subset of moves for checkmate
        for move in moves[:10]:
            g = Game(obs['board'])
            g.apply_move(move)
            if g.status == Game.CHECKMATE:
                return move

        # 2. Check for captures
        for move in moves:
            if game.board.get_piece(Game.xy2i(move[2:4])) != ' ':
                return move

        # 3. Check for queen promotions
        for move in moves:
            if "q" in move.lower():
                return move

        # 4. Random move if no checkmates or captures
        return random.choice(moves)
    except Exception as e:
        # If anything goes wrong, try to make a legal first move
        return "e2e4"
    
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
