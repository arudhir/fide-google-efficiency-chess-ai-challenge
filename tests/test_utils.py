# tests/test_utils.py
import chess
import chess.engine
import time
import random
import json
import dataclasses
from typing import Dict, List, Optional
from pathlib import Path

@dataclasses.dataclass
class GameResult:
    winner: str
    moves: int
    time_taken: float
    ending: str
    final_fen: str

@dataclasses.dataclass
class TestSession:
    """Test session results container"""
    bot_name: str
    timestamp: str
    random_results: List[GameResult]
    stockfish_results: List[GameResult]
    memory_usage: float
    avg_move_time: float

    def save(self, directory: Path):
        output = dataclasses.asdict(self)
        path = directory / f"test_session_{self.bot_name}_{self.timestamp}.json"
        directory.mkdir(exist_ok=True)
        with open(path, 'w') as f:
            json.dump(output, f, indent=2)


class RandomPlayer:
    def get_move(self, board: chess.Board) -> chess.Move:
        """Simple random move selector"""
        return random.choice(list(board.legal_moves))

class StockfishPlayer:
    def __init__(self, elo: int = 1200, time_limit: float = 0.1):
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.engine.configure({"Skill Level": elo // 100})
        self.time_limit = time_limit

    def get_move(self, board: chess.Board) -> chess.Move:
        """Get move from Stockfish with specified ELO and time limit"""
        result = self.engine.play(board, chess.engine.Limit(time=self.time_limit))
        return result.move

    def __del__(self):
        self.engine.quit()

def play_single_game(bot_func, opponent, bot_color: chess.Color) -> GameResult:
    """Play a single game and return detailed results"""
    board = chess.Board()
    moves = 0
    start_time = time.time()
    
    while not board.is_game_over() and moves < 200:  # 200 move limit
        is_bot_turn = (board.turn == bot_color)
        
        try:
            if is_bot_turn:
                obs = {'board': board.fen()}
                move = bot_func(obs)
                board.push_uci(move)
            else:
                move = opponent.get_move(board)
                board.push(move)
                
            moves += 1
            
        except Exception as e:
            print(f"Error during game: {e}")
            return GameResult(
                winner='opponent',
                moves=moves,
                time_taken=time.time() - start_time,
                ending='error',
                final_fen=board.fen()
            )
    
    # Determine game result
    if board.is_checkmate():
        winner = 'bot' if board.turn != bot_color else 'opponent'
        ending = 'checkmate'
    elif board.is_stalemate():
        winner = 'draw'
        ending = 'stalemate'
    elif board.is_fifty_moves():
        winner = 'draw'
        ending = 'fifty-move'
    elif board.is_repetition():
        winner = 'draw'
        ending = 'repetition'
    elif moves >= 200:
        winner = 'draw'
        ending = 'move-limit'
    else:
        winner = 'draw'
        ending = 'unknown'
    
    return GameResult(
        winner=winner,
        moves=moves,
        time_taken=time.time() - start_time,
        ending=ending,
        final_fen=board.fen()
    )

def measure_memory_usage(bot_func, num_moves: int = 10) -> float:
    """Measure memory usage over several moves"""
    import psutil
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    board = chess.Board()
    for _ in range(num_moves):
        obs = {'board': board.fen()}
        move = bot_func(obs)
        if move:
            board.push_uci(move)
            
    final_memory = process.memory_info().rss
    return (final_memory - initial_memory) / (1024 * 1024)  # Convert to MB