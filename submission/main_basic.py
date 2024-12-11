from Chessnut import Game
import random

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

def chess_bot(obs):
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
        for move in moves[:10]:
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

# def chess_bot(obs):
#     """
#     Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

#     Args:
#         obs: A dictionary with a 'board' key containing the FEN string of the current board state.

#     Returns:
#         A string representing the chosen move in UCI notation (e.g., "e2e4")
#     """
#     try:
#         # 0. Parse the current board state and generate legal moves using Chessnut library
#         game = Game(obs['board'])  # Changed from obs.board to obs['board']
#         moves = list(game.get_moves())

#         if not moves:  # No legal moves
#             return ""

#         # 1. Check a subset of moves for checkmate
#         for move in moves[:10]:
#             g = Game(obs['board'])
#             g.apply_move(move)
#             if g.status == Game.CHECKMATE:
#                 return move

#         # 2. Check for captures
#         for move in moves:
#             if game.board.get_piece(Game.xy2i(move[2:4])) != ' ':
#                 return move

#         # 3. Check for queen promotions
#         for move in moves:
#             if "q" in move.lower():
#                 return move

#         # 4. Random move if no checkmates or captures
#         return random.choice(moves)
#     except Exception as e:
#         # If anything goes wrong, try to make a legal first move
#         return "e2e4"

# from Chessnut import Game
# import random

# def get_checkmate_move(game, moves):
#     for move in moves:
#         temp_game = Game(game.board)  # Create a copy of the game
#         temp_game.apply_move(move)
#         if temp_game.status == Game.CHECKMATE:
#             return move
#     return None

# def get_capture_move(game, moves):
#     capture_moves = []
#     for move in moves:
#         target_square = move[2:4]
#         if game.board.get_piece(Game.xy2i(target_square)) != ' ':
#             capture_moves.append(move)
#     return capture_moves[0] if capture_moves else None

# def get_queen_promotion_move(moves):
#     for move in moves:
#         if "q" in move.lower():
#             return move
#     return None

# def attack_castled_king(game, moves):
#     """
#     Identify moves targeting squares around the castled king.
#     """
#     king_position = Game.xy2i(game.board.index('k')) if 'k' in game.board else None
#     attack_positions = [king_position + offset for offset in [-1, -9, 1, 9] if 0 <= king_position + offset < 64]
#     for move in moves:
#         if Game.xy2i(move[2:4]) in attack_positions:
#             return move
#     return None

# def find_open_file_moves(game, moves):
#     """
#     Suggest moves that utilize open files for rooks and queens.
#     """
#     open_files = []
#     for file in range(8):
#         if all(game.board[file + rank * 8] == ' ' for rank in range(8)):
#             open_files.append(file)
#     for move in moves:
#         if int(move[2]) in open_files:
#             return move
#     return None

# def get_safe_move(game, moves):
#     safe_moves = []
#     for move in moves:
#         temp_game = Game(game.board)  # Create a copy of the game
#         temp_game.apply_move(move)
#         if temp_game.status != Game.CHECK:
#             safe_moves.append(move)
#     return safe_moves[0] if safe_moves else None

# def chess_bot(obs):
#     """
#     Improved chess bot that prioritizes:
#     1. Checkmate
#     2. Captures
#     3. Queen promotion
#     4. Attacks on the castled king
#     5. Utilizing open files
#     6. Safe moves
#     7. Random move if no other criteria are met.

#     Args:
#         obs: An object with a 'board' attribute representing the current board state as a FEN string.

#     Returns:
#         A string representing the chosen move in UCI notation (e.g., "e2e4").
#     """
#     game = Game(obs.board)  # Assuming the input object has a `.board` attribute
#     moves = list(game.get_moves())

#     # 1. Check for Checkmate (Highest Priority)
#     checkmate_move = get_checkmate_move(game, moves)
#     if checkmate_move:
#         return checkmate_move

#     # 2. Capture opponent pieces
#     capture_move = get_capture_move(game, moves)
#     if capture_move:
#         return capture_move

#     # 3. Queen promotion
#     queen_promotion_move = get_queen_promotion_move(moves)
#     if queen_promotion_move:
#         return queen_promotion_move

#     # 4. Attack castled king
#     king_attack_move = attack_castled_king(game, moves)
#     if king_attack_move:
#         return king_attack_move

#     # 5. Utilize open files
#     open_file_move = find_open_file_moves(game, moves)
#     if open_file_move:
#         return open_file_move

#     # 6. Safe moves
#     safe_move = get_safe_move(game, moves)
#     if safe_move:
#         return safe_move

#     # 7. Random move if no other criteria met
#     return random.choice(moves)
