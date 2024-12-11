
import chess
import chess.engine

# submission/stockfish_evaluator.py
from chess_bot_naive import chess_bot
# from submission.chess_bot_naive import chess_bot

class StockfishEvaluator:
    def __init__(self, stockfish_path="stockfish"):
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        
    def play_game(self, bot_plays_white=True, elo=1200):
        """Play a game between our bot and Stockfish"""
        board = chess.Board()
        moves_made = 0
        
        # Configure Stockfish strength
        self.engine.configure({"Skill Level": elo // 100})
        
        while not board.is_game_over() and moves_made < 100:
            if board.turn == chess.WHITE and bot_plays_white or \
               board.turn == chess.BLACK and not bot_plays_white:
                # Our bot's turn
                obs = {'board': board.fen()}
                try:
                    move = chess_bot(obs)
                    board.push_uci(move)
                except Exception as e:
                    print(f"Bot error: {e}")
                    break
            else:
                # Stockfish's turn
                result = self.engine.play(board, chess.engine.Limit(time=0.1))
                board.push(result.move)
            
            moves_made += 1
        
        return self._get_game_result(board, bot_plays_white)
    
    def evaluate_bot(self, num_games=10, elo=1200):
        """Play multiple games and get statistics"""
        results = {'wins': 0, 'losses': 0, 'draws': 0}
        
        for i in range(num_games):
            # Alternate colors
            bot_plays_white = (i % 2 == 0)
            result = self.play_game(bot_plays_white, elo)
            results[result] += 1
            print(f"Game {i+1}: {result}")
            
        return results
    
    def _get_game_result(self, board, bot_plays_white):
        if board.is_checkmate():
            if (board.turn == chess.BLACK and bot_plays_white) or \
               (board.turn == chess.WHITE and not bot_plays_white):
                return 'wins'
            return 'losses'
        return 'draws'
    
    def __del__(self):
        self.engine.quit()

# Example usage
if __name__ == "__main__":
    evaluator = StockfishEvaluator()
    print("Testing bot against Stockfish (ELO 1200)...")
    results = evaluator.evaluate_bot(num_games=10, elo=1200)
    print("\nResults:")
    print(f"Wins: {results['wins']}")
    print(f"Draws: {results['draws']}")
    print(f"Losses: {results['losses']}")