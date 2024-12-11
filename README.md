# fide-google-efficiency-chess-ai-challenge

Run in resource-constrained environment
```bash
$ docker build -t chess-agent .
$ docker run --rm --cpus=1 chess_agent

Filename: submissions/main.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     6     60.6 MiB     60.6 MiB           1   @profile
     7                                         def chess_bot(fen):
     8                                             """
     9                                             Improved chess bot that prioritizes:
    10                                             1. Checkmate
    11                                             2. Captures
    12                                             3. Queen promotion
    13                                             4. Piece Safety
    14                                             5. Random move if no other criteria are met.
    15                                         
    16                                             Args:
    17                                                 fen: A string representing the current board state in FEN format.
    18                                         
    19                                             Returns:
    20                                                 A string representing the chosen move in UCI notation (e.g., "e2e4").
    21                                             """
    22     60.6 MiB      0.0 MiB           1       board = chess.Board(fen)
    23                                         
    24                                             # 1. Check for Checkmate (Highest Priority)
    25     60.6 MiB      0.0 MiB           1       checkmate_move = get_checkmate_move(board)
    26     60.6 MiB      0.0 MiB           1       if checkmate_move:
    27                                                 return checkmate_move
    28                                         
    29                                             # 2. Capture opponent pieces
    30     60.6 MiB      0.0 MiB           1       capture_move = get_capture_move(board)
    31     60.6 MiB      0.0 MiB           1       if capture_move:
    32                                                 return capture_move
    33                                         
    34                                             # 3. Queen promotion
    35     60.6 MiB      0.0 MiB           1       queen_promotion_move = get_queen_promotion_move(board)
    36     60.6 MiB      0.0 MiB           1       if queen_promotion_move:
    37                                                 return queen_promotion_move
    38                                         
    39                                             # 4. Piece Safety
    40     60.6 MiB      0.0 MiB           1       safe_move = get_safe_move(board)
    41     60.6 MiB      0.0 MiB           1       if safe_move:
    42     60.6 MiB      0.0 MiB           1           return safe_move
    43                                         
    44                                             # 5. Random move if no other criteria met
    45                                             return random.choice(list(board.legal_moves)).uci()


Chosen move: d2d4
```

