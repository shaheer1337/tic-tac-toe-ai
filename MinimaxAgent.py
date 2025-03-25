import numpy as np
from typing import Tuple, Optional
from TicTacToeGame import TicTacToe

class MinimaxAgent:
    def __init__(self, player: int):
        """
        Initialize the Minimax agent.
        Args:
            player: 1 for X (maximizing player), -1 for O (minimizing player)
        """
        self.player = player
        
    def get_move(self, game: TicTacToe) -> Tuple[int, int]:
        """
        Get the best move for the current game state using minimax with alpha-beta pruning.
        Args:
            game: Current TicTacToe game instance
        Returns:
            Tuple[int, int]: Best move as (row, col)
        """
        best_score = float('-inf') if self.player == 1 else float('inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for move in game.get_valid_moves():
            # Make move
            game.make_move(move[0], move[1])
            
            # Get score for this move
            score = self._minimax(game, 0, alpha, beta, self.player == -1)
            
            # Undo move
            game.board[move[0], move[1]] = 0
            game.game_over = False
            game.winner = None
            game.current_player = self.player
            
            # Update best move
            if self.player == 1:
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
        
        return best_move
    
    def _minimax(self, game: TicTacToe, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        """
        Minimax algorithm with alpha-beta pruning.
        Args:
            game: Current game state
            depth: Current depth in the game tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if current player is maximizing
        Returns:
            float: Best score for current state
        """
        # Check terminal states
        if game.is_terminal():
            reward = game.get_reward()
            # Adjust reward based on depth to prefer shorter paths to victory
            return reward * (1 - depth * 0.1)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in game.get_valid_moves():
                game.make_move(move[0], move[1])
                eval = self._minimax(game, depth + 1, alpha, beta, False)
                game.board[move[0], move[1]] = 0
                game.game_over = False
                game.winner = None
                game.current_player = 1
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in game.get_valid_moves():
                game.make_move(move[0], move[1])
                eval = self._minimax(game, depth + 1, alpha, beta, True)
                game.board[move[0], move[1]] = 0
                game.game_over = False
                game.winner = None
                game.current_player = -1
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

# Example usage
if __name__ == "__main__":
    # Create game and agents
    game = TicTacToe()
    x_agent = MinimaxAgent(player=1)  # X player
    o_agent = MinimaxAgent(player=-1)  # O player
    
    print("Starting game with Minimax agents:")
    print(game)
    
    # Play game
    while not game.is_terminal():
        current_agent = x_agent if game.current_player == 1 else o_agent
        move = current_agent.get_move(game)
        game.make_move(move[0], move[1])
        print(f"\nAfter move ({move[0]}, {move[1]}):")
        print(game)
    
    # Print result
    winner = "X" if game.winner == 1 else "O" if game.winner == -1 else "Draw"
    print(f"\nGame Over! Winner: {winner}") 