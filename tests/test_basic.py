
# import pytest
# import chess
# import sys
# from pathlib import Path

# # # Add the project root to Python path
# # project_root = Path(__file__).parent.parent
# # sys.path.append(str(project_root))

# from submission.submission import chess_bot  # Now importing from the package



# def test_valid_move_format():
#     """Test that moves returned are in valid UCI format"""
#     observation = {'board': chess.STARTING_FEN}
#     move = chess_bot(observation)
    
#     # Check move format (e.g., "e2e4")
#     assert isinstance(move, str)
#     assert len(move) >= 4
#     assert all(c in 'abcdefgh12345678' for c in move[:4])

# def test_legal_moves(sample_positions):
#     """Test that all returned moves are legal in given positions"""
#     for fen in sample_positions:
#         observation = {'board': fen}
#         move = chess_bot(observation)
        
#         board = chess.Board(fen)
#         chess_move = chess.Move.from_uci(move)
#         assert chess_move in board.legal_moves

# def test_error_handling():
#     """Test bot handles invalid positions gracefully"""
#     # Invalid FEN
#     observation = {'board': 'invalid_fen'}
#     move = chess_bot(observation)
#     assert isinstance(move, str)
    
#     # Missing board key
#     observation = {}
#     move = chess_bot(observation)
#     assert isinstance(move, str)

# def test_memory_usage(sample_positions):
#     """Test memory usage stays within competition limits"""
#     import resource
#     import psutil
    
#     for fen in sample_positions:
#         observation = {'board': fen}
        
#         # Get initial memory usage
#         process = psutil.Process()
#         initial_memory = process.memory_info().rss
        
#         # Make move
#         move = chess_bot(observation)
        
#         # Check memory usage
#         final_memory = process.memory_info().rss
#         memory_used = (final_memory - initial_memory) / (1024 * 1024)  # Convert to MB
        
#         assert memory_used < 5  # Competition limit is 5MB

# # tests/test_stockfish.py
# import pytest
# import chess
# from submission import chess_bot

# def test_against_stockfish(stockfish_engine):
#     """Test bot performance against Stockfish at different ELO levels"""
#     results = {'wins': 0, 'losses': 0, 'draws': 0}
    
#     def play_game(engine_elo=1200):
#         board = chess.Board()
        
#         # Configure Stockfish
#         stockfish_engine.configure({"Skill Level": engine_elo // 100})
        
#         while not board.is_game_over():
#             # Bot's move
#             observation = {'board': board.fen()}
#             move = chess_bot(observation)
#             board.push(chess.Move.from_uci(move))
            
#             if board.is_game_over():
#                 break
                
#             # Stockfish's move
#             result = stockfish_engine.play(board, chess.engine.Limit(time=0.1))
#             board.push(result.move)
        
#         return board.outcome()
    
#     # Play multiple games
#     for _ in range(5):
#         outcome = play_game(engine_elo=1200)
#         if outcome.winner is True:  # Bot wins
#             results['wins'] += 1
#         elif outcome.winner is False:  # Bot loses
#             results['losses'] += 1
#         else:  # Draw
#             results['draws'] += 1
    
#     # Assert bot isn't losing every game
#     assert results['wins'] + results['draws'] > 0

# # tests/test_performance.py
# import pytest
# import chess
# import time
# from submission import chess_bot

# def test_move_time():
#     """Test that moves are made within time constraints"""
#     observation = {'board': chess.STARTING_FEN}
    
#     start_time = time.time()
#     move = chess_bot(observation)
#     elapsed_time = time.time() - start_time
    
#     # Competition has 0.1s delay
#     assert elapsed_time < 0.1

# def test_consecutive_moves():
#     """Test performance over multiple consecutive moves"""
#     board = chess.Board()
#     times = []
    
#     # Play 10 moves
#     for _ in range(10):
#         observation = {'board': board.fen()}
        
#         start_time = time.time()
#         move = chess_bot(observation)
#         elapsed_time = time.time() - start_time
        
#         times.append(elapsed_time)
#         board.push(chess.Move.from_uci(move))
    
#     # Check average and max times
#     avg_time = sum(times) / len(times)
#     max_time = max(times)
    
#     assert avg_time < 0.05  # Average should be well under limit
#     assert max_time < 0.1  # No single move should exceed limit
