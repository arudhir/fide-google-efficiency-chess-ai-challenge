# fide-google-efficiency-chess-ai-challenge

Evaluate against a random player and Stockfish 1200
```
$ make test

uv run pytest tests -v -s
=================================== test session starts ====================================
platform darwin -- Python 3.11.9, pytest-8.3.4, pluggy-1.5.0 -- /Users/aru/Development/fide-google-efficiency-chess-ai-challenge/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/aru/Development/fide-google-efficiency-chess-ai-challenge
configfile: pyproject.toml
collected 2 items                                                                          

tests/test_benchmarks.py::test_basic_bot 
==================================================
Testing basic bot
==================================================

📊 Random Player Games:

Game 1 - Bot playing as White
Result: draw in 200 moves (other)

Game 2 - Bot playing as Black
Result: bot in 82 moves (checkmate)

Game 3 - Bot playing as White
Result: bot in 103 moves (checkmate)

Game 4 - Bot playing as Black
Result: draw in 54 moves (other)

Game 5 - Bot playing as White
Result: bot in 91 moves (checkmate)

Game 6 - Bot playing as Black
Result: bot in 22 moves (checkmate)

Game 7 - Bot playing as White
Result: bot in 45 moves (checkmate)

Game 8 - Bot playing as Black
Result: draw in 200 moves (other)

Game 9 - Bot playing as White
Result: bot in 79 moves (checkmate)

Game 10 - Bot playing as Black
Result: bot in 90 moves (checkmate)

Random Games Summary:
Wins: 7/10 (70.0%)
Draws: 3/10 (30.0%)

🤖 Stockfish Games (ELO 1200):

Game 1 - Bot playing as White
Result: opponent in 44 moves (checkmate)

Game 2 - Bot playing as Black
Result: opponent in 27 moves (checkmate)

Game 3 - Bot playing as White
Result: opponent in 12 moves (checkmate)

Game 4 - Bot playing as Black
Result: opponent in 31 moves (checkmate)

Game 5 - Bot playing as White
Result: opponent in 36 moves (checkmate)

Stockfish Games Summary:
Wins: 0/5 (0.0%)
Draws: 0/5 (0.0%)

⚡ Performance Metrics:
Memory Usage: 0.02 MB
Average Move Time: 18.1 ms

Results saved to: test_results/test_session_basic_20241211_175723.json
PASSED
tests/test_benchmarks.py::test_hybrid_bot 
==================================================
Testing hybrid bot
==================================================

📊 Random Player Games:

Game 1 - Bot playing as White
Result: opponent in 70 moves (checkmate)

Game 2 - Bot playing as Black
Result: bot in 128 moves (checkmate)

Game 3 - Bot playing as White
Result: bot in 163 moves (checkmate)

Game 4 - Bot playing as Black
Result: draw in 136 moves (other)

Game 5 - Bot playing as White
Result: draw in 200 moves (other)

Game 6 - Bot playing as Black
Result: bot in 154 moves (checkmate)

Game 7 - Bot playing as White
Result: opponent in 104 moves (checkmate)

Game 8 - Bot playing as Black
Result: draw in 126 moves (other)

Game 9 - Bot playing as White
Result: draw in 200 moves (other)

Game 10 - Bot playing as Black
Result: draw in 200 moves (other)

Random Games Summary:
Wins: 3/10 (30.0%)
Draws: 5/10 (50.0%)

🤖 Stockfish Games (ELO 1200):

Game 1 - Bot playing as White
Result: opponent in 10 moves (checkmate)

Game 2 - Bot playing as Black
Result: opponent in 25 moves (checkmate)

Game 3 - Bot playing as White
Result: opponent in 32 moves (checkmate)

Game 4 - Bot playing as Black
Result: opponent in 47 moves (checkmate)

Game 5 - Bot playing as White
Result: opponent in 30 moves (checkmate)

Stockfish Games Summary:
Wins: 0/5 (0.0%)
Draws: 0/5 (0.0%)

⚡ Performance Metrics:
Memory Usage: 0.00 MB
Average Move Time: 24.4 ms

Results saved to: test_results/test_session_hybrid_20241211_175740.json
PASSED
```