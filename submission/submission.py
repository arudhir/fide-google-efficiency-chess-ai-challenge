# submission/submission.py
from Chessnut import Game
import random

def chess_bot_basic(obs):
    """
    Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

    Args:
        obs: An object with a 'board' attribute representing the current board state as a FEN string.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    # 0. Parse the current board state and generate legal moves using Chessnut library
    game = Game(obs['board'])
    moves = list(game.get_moves())

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

from Chessnut import Game
import random

# Piece values (same as before)
PIECE_VALUES = {
    'P': 100,   # Pawn
    'N': 320,   # Knight
    'B': 330,   # Bishop
    'R': 500,   # Rook
    'Q': 900,   # Queen
    'K': 20000  # King
}

# Center squares in Chessnut coordinates
CENTER_SQUARES = [
    Game.xy2i('e4'), Game.xy2i('d4'),
    Game.xy2i('e5'), Game.xy2i('d5')
]

def evaluate_move(game, move):
    """Evaluate a move based on multiple criteria"""
    score = 0
    
    # Make move on a copy of the game
    test_game = Game(game.board.fen)
    test_game.apply_move(move)
    
    # Convert coordinates
    from_square = Game.xy2i(move[0:2])
    to_square = Game.xy2i(move[2:4])
    
    # 1. Checkmate is best
    if test_game.status == Game.CHECKMATE:
        return 10000
        
    # 2. Capture value
    captured_piece = game.board.get_piece(to_square)
    if captured_piece != ' ':
        score += PIECE_VALUES.get(captured_piece.upper(), 0)
    
    # 3. Queen promotion
    if 'q' in move.lower():
        score += 800
        
    # 4. Center control
    piece = test_game.board.get_piece(to_square)
    if piece != ' ':
        if to_square in CENTER_SQUARES:
            score += 30
    
    # 5. Pawn structure
    if piece.upper() == 'P':
        file_idx = to_square % 8
        # Check for doubled pawns
        pawns_in_file = 0
        for rank in range(8):
            square = rank * 8 + file_idx
            p = test_game.board.get_piece(square)
            if p.upper() == 'P' and p.isupper() == piece.isupper():
                pawns_in_file += 1
        if pawns_in_file > 1:
            score -= 30
            
        # Check for isolated pawns
        has_adjacent_pawn = False
        for adj_file in [file_idx - 1, file_idx + 1]:
            if 0 <= adj_file < 8:
                for rank in range(8):
                    square = rank * 8 + adj_file
                    p = test_game.board.get_piece(square)
                    if p.upper() == 'P' and p.isupper() == piece.isupper():
                        has_adjacent_pawn = True
        if not has_adjacent_pawn:
            score -= 20
    
    # 6. Rook on open file
    if piece.upper() == 'R':
        file_idx = to_square % 8
        open_file = True
        for rank in range(8):
            square = rank * 8 + file_idx
            p = test_game.board.get_piece(square)
            if p.upper() == 'P':
                open_file = False
                break
        if open_file:
            score += 50
    
    return score

def chess_bot(obs):
    """
    Enhanced chess bot with sophisticated position evaluation.
    """
    try:
        # Parse the current board state
        game = Game(obs['board'])
        moves = list(game.get_moves())
        
        if not moves:
            return ""
            
        # Evaluate all possible moves
        move_scores = []
        for move in moves:
            score = evaluate_move(game, move)
            move_scores.append((move, score))
        
        # Sort moves by score
        move_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select from top 3 moves to add some randomness
        top_moves = move_scores[:3]
        if top_moves:
            # Weight selection by score
            total_score = sum(max(score, 1) for _, score in top_moves)
            rand_val = random.uniform(0, total_score)
            current_sum = 0
            
            for move, score in top_moves:
                current_sum += max(score, 1)
                if current_sum > rand_val:
                    return move
            
            # Fallback to best move
            return top_moves[0][0]
            
        # Fallback to random move
        return random.choice(moves)
        
    except Exception as e:
        # Emergency fallback - try to make any valid move
        try:
            game = Game(obs['board'])
            moves = list(game.get_moves())
            if moves:
                return random.choice(moves)
            return ""
        except:
            return ""



















# def evaluate_move(board, move, is_endgame=False):
#     """
#     Evaluate a move based on multiple criteria and return a score.
#     Higher scores are better.
#     """
#     score = 0
    
#     # Make move temporarily to evaluate position
#     board.push(move)
    
#     try:
#         # Immediate winning moves (highest priority)
#         if board.is_checkmate():
#             score += 10000
            
#         # Material gain from captures
#         if board.is_capture(move):
#             captured_piece = board.piece_at(move.to_square)
#             if captured_piece:
#                 piece_values = {
#                     chess.PAWN: 100,
#                     chess.KNIGHT: 320,
#                     chess.BISHOP: 330,
#                     chess.ROOK: 500,
#                     chess.QUEEN: 900,
#                     chess.KING: 20000
#                 }
#                 score += piece_values.get(captured_piece.piece_type, 0)
        
#         # Pawn promotion
#         if move.promotion == chess.QUEEN:
#             score += 800
        
#         # King attack potential
#         enemy_king_square = board.king(not board.turn)
#         if enemy_king_square:
#             king_attackers = len([
#                 square for square in chess.SQUARES
#                 if board.is_attacked_by(board.turn, square) and 
#                 abs(chess.square_file(square) - chess.square_file(enemy_king_square)) <= 2 and
#                 abs(chess.square_rank(square) - chess.square_rank(enemy_king_square)) <= 2
#             ])
#             score += king_attackers * 50
        
#         # Control of center
#         center_squares = [27, 28, 35, 36]  # e4, d4, e5, d5
#         center_control = sum(1 for square in center_squares if board.is_attacked_by(board.turn, square))
#         score += center_control * 30
        
#         # Piece mobility
#         mobility = len(list(board.legal_moves))
#         score += mobility * 5
        
#         # Pawn structure
#         doubled_pawns = 0
#         isolated_pawns = 0
#         for file_idx in range(8):
#             pawns_in_file = 0
#             has_friendly_pawns_adjacent = False
            
#             for rank_idx in range(8):
#                 square = chess.square(file_idx, rank_idx)
#                 piece = board.piece_at(square)
#                 if piece and piece.piece_type == chess.PAWN and piece.color == board.turn:
#                     pawns_in_file += 1
                    
#                     # Check adjacent files for friendly pawns
#                     for adj_file in [file_idx - 1, file_idx + 1]:
#                         if 0 <= adj_file < 8:
#                             for rank in range(8):
#                                 adj_square = chess.square(adj_file, rank)
#                                 adj_piece = board.piece_at(adj_square)
#                                 if adj_piece and adj_piece.piece_type == chess.PAWN and adj_piece.color == board.turn:
#                                     has_friendly_pawns_adjacent = True
                                    
#             if pawns_in_file > 1:
#                 doubled_pawns += 1
#             if pawns_in_file > 0 and not has_friendly_pawns_adjacent:
#                 isolated_pawns += 1
                
#         score -= (doubled_pawns * 30 + isolated_pawns * 20)
        
#         # Rook on open file
#         if board.piece_at(move.from_square) and board.piece_at(move.from_square).piece_type == chess.ROOK:
#             file_idx = chess.square_file(move.to_square)
#             open_file = True
#             for rank_idx in range(8):
#                 square = chess.square(file_idx, rank_idx)
#                 piece = board.piece_at(square)
#                 if piece and piece.piece_type == chess.PAWN:
#                     open_file = False
#                     break
#             if open_file:
#                 score += 50
        
#         # Piece coordination
#         attacking_pieces = len([
#             square for square in chess.SQUARES
#             if board.is_attacked_by(board.turn, square)
#         ])
#         score += attacking_pieces * 5
        
#         # Safety of own king
#         own_king_square = board.king(board.turn)
#         if own_king_square:
#             king_attackers = len([
#                 square for square in chess.SQUARES
#                 if board.is_attacked_by(not board.turn, square) and 
#                 abs(chess.square_file(square) - chess.square_file(own_king_square)) <= 2 and
#                 abs(chess.square_rank(square) - chess.square_rank(own_king_square)) <= 2
#             ])
#             score -= king_attackers * 60
            
#     finally:
#         board.pop()
        
#     return score

# def chess_bot(observation):
#     """
#     Chess bot that evaluates positions using multiple criteria.
    
#     Args:
#         observation: An object with a 'board' attribute representing the current board state in FEN format.
    
#     Returns:
#         A string representing the chosen move in UCI notation (e.g., "e2e4").
#     """
#     board = chess.Board(observation['board'])
    
#     # Determine game phase
#     piece_count = len(board.piece_map())
#     is_endgame = piece_count <= 12
    
#     # Evaluate all legal moves
#     best_score = float('-inf')
#     best_moves = []
    
#     for move in board.legal_moves:
#         score = evaluate_move(board, move, is_endgame)
        
#         if score > best_score:
#             best_score = score
#             best_moves = [move]
#         elif score == best_score:
#             best_moves.append(move)
    
#     # Choose randomly among equally good moves
#     chosen_move = random.choice(best_moves)
#     return chosen_move.uci()

import chess
import random

def chess_bot(observation):
    """
    Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

    Args:
        observation: An object with a 'board' attribute representing the current board state in FEN format.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4").
    """
    try:
        # Parse the board state
        board = chess.Board(observation['board'])
        legal_moves = list(board.legal_moves)
        
        if not legal_moves:
            return None
            
        # 1. Check for immediate checkmate
        # Only check first 10 moves to save computation
        for move in legal_moves[:10]:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return move.uci()
            board.pop()
            
        # 2. Check for captures
        for move in legal_moves:
            if board.is_capture(move):
                return move.uci()
                
        # 3. Check for queen promotions
        for move in legal_moves:
            if move.promotion == chess.QUEEN:
                return move.uci()
                
        # 4. Random move if no better options found
        return random.choice(legal_moves).uci()
        
    except Exception as e:
        # Emergency fallback - make any legal move
        try:
            board = chess.Board(observation['board'])
            return random.choice(list(board.legal_moves)).uci()
        except:
            return 'e2e4'