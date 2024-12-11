# tests/test_benchmarks.py
import pytest
import chess
import chess.engine
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .test_utils import (
    GameResult,  # Added this import
    TestSession, 
    RandomPlayer, 
    StockfishPlayer
)
def run_test_session(bot_func, name: str, save_results: bool = True):
    """Utility function to run a full test session"""
    print(f"\n{'='*50}")
    print(f"Testing {name} bot")
    print(f"{'='*50}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Test against random player
    print("\n📊 Random Player Games:")
    random_player = RandomPlayer()
    random_results = []
    
    for i in range(10):
        bot_color = chess.WHITE if i % 2 == 0 else chess.BLACK
        print(f"\nGame {i+1} - Bot playing as {'White' if bot_color else 'Black'}")
        result = play_single_game(bot_func, random_player, bot_color)
        random_results.append(result)
        print(f"Result: {result.winner} in {result.moves} moves ({result.ending})")
    
    # Summarize random games
    random_wins = sum(1 for r in random_results if r.winner == 'bot')
    random_draws = sum(1 for r in random_results if r.winner == 'draw')
    print(f"\nRandom Games Summary:")
    print(f"Wins: {random_wins}/10 ({random_wins/10:.1%})")
    print(f"Draws: {random_draws}/10 ({random_draws/10:.1%})")
    
    # Test against Stockfish
    print("\n🤖 Stockfish Games (ELO 1200):")
    try:
        stockfish = StockfishPlayer(elo=1200)
        stockfish_results = []
        
        for i in range(5):
            bot_color = chess.WHITE if i % 2 == 0 else chess.BLACK
            print(f"\nGame {i+1} - Bot playing as {'White' if bot_color else 'Black'}")
            result = play_single_game(bot_func, stockfish, bot_color)
            stockfish_results.append(result)
            print(f"Result: {result.winner} in {result.moves} moves ({result.ending})")
        
        # Summarize Stockfish games
        stockfish_wins = sum(1 for r in stockfish_results if r.winner == 'bot')
        stockfish_draws = sum(1 for r in stockfish_results if r.winner == 'draw')
        print(f"\nStockfish Games Summary:")
        print(f"Wins: {stockfish_wins}/5 ({stockfish_wins/5:.1%})")
        print(f"Draws: {stockfish_draws}/5 ({stockfish_draws/5:.1%})")
        
    except Exception as e:
        print(f"\n❌ Error setting up Stockfish: {e}")
        print("Make sure Stockfish is installed and accessible")
        stockfish_results = []
    
    # Performance metrics
    print("\n⚡ Performance Metrics:")
    memory_usage = measure_memory_usage(bot_func)
    move_times = measure_move_times(bot_func)
    avg_time = sum(move_times) / len(move_times)
    print(f"Memory Usage: {memory_usage:.2f} MB")
    print(f"Average Move Time: {avg_time*1000:.1f} ms")
    
    session = TestSession(
        bot_name=name,
        timestamp=timestamp,
        random_results=random_results,
        stockfish_results=stockfish_results,
        memory_usage=memory_usage,
        avg_move_time=avg_time
    )
    
    if save_results:
        output_dir = Path('test_results')
        output_dir.mkdir(exist_ok=True)
        session.save(output_dir)
        print(f"\nResults saved to: {output_dir}/test_session_{name}_{timestamp}.json")
    
    return session

# Add option to run tests with more output
def test_basic_bot(capsys):
    """Test basic bot implementation"""
    from submission.bots.basic_bot import chess_bot_basic
    with capsys.disabled():
        results = run_test_session(chess_bot_basic, "basic")
    
    # Assertions
    random_wins = sum(1 for r in results.random_results if r.winner == 'bot')
    win_rate = random_wins / len(results.random_results)
    assert win_rate >= 0.2, f"Win rate against random too low: {win_rate:.2%}"
    assert results.avg_move_time < 0.1, f"Moves taking too long: {results.avg_move_time:.3f}s"
    assert results.memory_usage < 5, f"Using too much memory: {results.memory_usage:.2f}MB"


def play_single_game(bot_func, opponent, bot_color):
    board = chess.Board()
    moves = 0
    start_time = time.time()
    
    while not board.is_game_over() and moves < 200:
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
    
    time_taken = time.time() - start_time
    
    if board.is_checkmate():
        winner = 'bot' if board.turn != bot_color else 'opponent'
        ending = 'checkmate'
    else:
        winner = 'draw'
        ending = 'other'
        
    return GameResult(
        winner=winner,
        moves=moves,
        time_taken=time_taken,
        ending=ending,
        final_fen=board.fen()
    )

def measure_memory_usage(bot_func, num_moves=10):
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
    return (final_memory - initial_memory) / (1024 * 1024)

def measure_move_times(bot_func, num_moves=10):
    times = []
    board = chess.Board()
    
    for _ in range(num_moves):
        start = time.time()
        move = bot_func({'board': board.fen()})
        times.append(time.time() - start)
        if move:
            board.push_uci(move)
    
    return times

# Actual test functions


def test_hybrid_bot():
    """Test hybrid bot implementation"""
    from submission.bots.hybrid_bot import chess_bot_hybrid
    results = run_test_session(chess_bot_hybrid, "hybrid")
    
    # Assertions
    random_wins = sum(1 for r in results.random_results if r.winner == 'bot')
    win_rate = random_wins / len(results.random_results)
    assert win_rate >= 0.2, f"Win rate against random too low: {win_rate:.2%}"
    assert results.avg_move_time < 0.1, f"Moves taking too long: {results.avg_move_time:.3f}s"
    assert results.memory_usage < 5, f"Using too much memory: {results.memory_usage:.2f}MB"