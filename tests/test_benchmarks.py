# tests/test_benchmarks.py
import pytest
import chess
import chess.engine
from submission.submission import chess_bot
import random
import time

class RandomPlayer:
    def get_move(self, board):
        return random.choice(list(board.legal_moves))

class StockfishPlayer:
    def __init__(self, elo=1200):
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.engine.configure({"Skill Level": elo // 100})
        
    def get_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        return result.move
        
    def __del__(self):
        self.engine.quit()

def play_game(bot_color, opponent):
    """Play a full game between our bot and an opponent"""
    board = chess.Board()
    moves_made = 0
    
    while not board.is_game_over() and moves_made < 100:
        if board.turn == bot_color:
            # Our bot's turn
            obs = {'board': board.fen()}
            try:
                move = chess_bot(obs)
                board.push_uci(move)
            except Exception as e:
                print(f"Bot error: {e}")
                return 'opponent'
        else:
            # Opponent's turn
            move = opponent.get_move(board)
            board.push(move)
        
        moves_made += 1
    
    if board.is_checkmate():
        return 'bot' if board.turn != bot_color else 'opponent'
    return 'draw'

def test_against_random():
    """Test bot performance against random moves"""
    results = {'bot': 0, 'opponent': 0, 'draw': 0}
    opponent = RandomPlayer()
    
    start_time = time.time()
    
    for i in range(10):  # Play 10 games
        bot_color = chess.WHITE if i % 2 == 0 else chess.BLACK
        result = play_game(bot_color, opponent)
        results[result] += 1
        print(f"Game {i+1}: {result}")
    
    elapsed = time.time() - start_time
    print(f"\nRandom Player Results (took {elapsed:.2f}s):")
    print(f"Wins: {results['bot']}")
    print(f"Losses: {results['opponent']}")
    print(f"Draws: {results['draw']}")
    
    win_rate = results['bot'] / (results['bot'] + results['opponent'] + results['draw'])
    assert win_rate >= 0.4, f"Win rate against random too low: {win_rate:.2%}"

def test_against_stockfish():
    """Test bot performance against Stockfish"""
    results = {'bot': 0, 'opponent': 0, 'draw': 0}
    opponent = StockfishPlayer(elo=0)
    
    start_time = time.time()
    
    for i in range(5):  # Play 5 games (Stockfish games take longer)
        bot_color = chess.WHITE if i % 2 == 0 else chess.BLACK
        result = play_game(bot_color, opponent)
        results[result] += 1
        print(f"Game {i+1}: {result}")
    
    elapsed = time.time() - start_time
    print(f"\nStockfish Results (took {elapsed:.2f}s):")
    print(f"Wins: {results['bot']}")
    print(f"Losses: {results['opponent']}")
    print(f"Draws: {results['draw']}")
    
    not_loss_rate = (results['bot'] + results['draw']) / (results['bot'] + results['opponent'] + results['draw'])
    assert not_loss_rate > 0.2, f"Performance against Stockfish too low: {not_loss_rate:.2%}"

def test_time_limit():
    """Test that moves are made within time limit"""
    board = chess.Board()
    obs = {'board': board.fen()}
    
    start_time = time.time()
    move = chess_bot(obs)
    elapsed = time.time() - start_time
    
    assert elapsed < 0.1, f"Move took too long: {elapsed} seconds"

def test_memory_usage():
    """Test memory usage stays within limits"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Make some moves
    board = chess.Board()
    for _ in range(5):
        obs = {'board': board.fen()}
        move = chess_bot(obs)
        if move:
            board.push_uci(move)
    
    final_memory = process.memory_info().rss
    memory_used_mb = (final_memory - initial_memory) / (1024 * 1024)
    
    assert memory_used_mb < 5, f"Used too much memory: {memory_used_mb}MB"