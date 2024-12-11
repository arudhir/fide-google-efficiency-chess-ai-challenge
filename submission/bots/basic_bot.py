# submission/bots/basic_bot.py
from Chessnut import Game
import random

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
