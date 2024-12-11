from Chessnut import Game
import random

# Piece values
PIECE_VALUES = {
    'P': 100,   # Pawn
    'N': 320,   # Knight
    'B': 330,   # Bishop
    'R': 500,   # Rook
    'Q': 900,   # Queen
    'K': 20000  # King
}

# Position values for pieces (higher value = better square)
PIECE_POSITION_VALUES = {
    # Pawns prefer advancing and controlling center
    'P': [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ],
    # Knights prefer central positions
    'N': [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]
}

def evaluate_piece_position(piece, square_idx, is_endgame):
    """Evaluate the positional value of a piece on a square"""
    if piece.upper() not in PIECE_POSITION_VALUES:
        return 0
        
    position_value = PIECE_POSITION_VALUES[piece.upper()][square_idx]
    return position_value if piece.isupper() else -position_value

def evaluate_position(game):
    """Evaluate the current position"""
    score = 0
    piece_count = 0
    
    # Count material and pieces
    for idx, piece in enumerate(game.board.get_pieces()):
        if piece != ' ':
            piece_count += 1
            # Material value
            value = PIECE_VALUES.get(piece.upper(), 0)
            score += value if piece.isupper() else -value
            
            # Position value
            is_endgame = piece_count <= 10
            score += evaluate_piece_position(piece, idx, is_endgame)
    
    return score

def evaluate_move(game, move):
    """Evaluate a potential move"""
    score = 0
    
    # Make move on a copy of the game
    test_game = Game(game.board.fen)
    test_game.apply_move(move)
    
    # Basic move scoring
    to_square = Game.xy2i(move[2:4])
    from_square = Game.xy2i(move[0:2])
    
    # Checkmate is best
    if test_game.status == Game.CHECKMATE:
        return 100000
    
    # Capture value
    captured_piece = game.board.get_piece(to_square)
    if captured_piece != ' ':
        score += PIECE_VALUES.get(captured_piece.upper(), 0)
    
    # Promotion value
    if 'q' in move.lower():
        score += 800
    
    # Position evaluation
    score += evaluate_position(test_game) - evaluate_position(game)
    
    return score

def chess_bot(obs):
    """
    Enhanced chess bot that considers material value, position, and common chess principles.

    Args:
        obs: A dictionary with a 'board' key containing the FEN string of the current board state.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    try:
        # Parse the current board state
        game = Game(obs['board'])
        legal_moves = list(game.get_moves())
        
        if not legal_moves:
            return ""
            
        # Evaluate all possible moves
        move_scores = []
        for move in legal_moves:
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
            
        # Fallback to random LEGAL move
        return random.choice(legal_moves)
        
    except Exception as e:
        # Emergency fallback - return a legal move from initial position
        try:
            game = Game(obs['board'])
            legal_moves = list(game.get_moves())
            if legal_moves:
                return random.choice(legal_moves)
            return ""
        except:
            return ""
