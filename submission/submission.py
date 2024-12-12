# submission/submission.py
from Chessnut import Game
import random

# submission/submission.py
from .bots.basic_bot import chess_bot_basic
from .bots.hybrid_bot import chess_bot_hybrid

# Choose which bot to use as the main submission
chess_bot = chess_bot_basic  # or chess_bot_hybrid