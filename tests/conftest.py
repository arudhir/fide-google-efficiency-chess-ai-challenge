import pytest
import chess
import chess.engine
import random

@pytest.fixture
def sample_positions():
    """Provide a set of test positions in FEN notation"""
    return [
        chess.STARTING_FEN,
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",  # Common opening
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",  # Complex middlegame
        "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"  # Endgame position
    ]

# tests/conftest.py
import pytest
import chess.engine

@pytest.fixture
def stockfish():
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    try:
        yield engine
    finally:
        engine.quit()

@pytest.fixture
def test_positions():
    return [
        chess.STARTING_FEN,
        # Add more test positions
    ]
