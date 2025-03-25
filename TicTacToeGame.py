import numpy as np
from typing import List, Tuple, Optional

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  # 1 for X, -1 for O
        self.game_over = False
        self.winner = None
        
    def make_move(self, row: int, col: int) -> bool:
        """Make a move on the board. Returns True if move was valid, False otherwise."""
        if self.game_over or not (0 <= row < 3 and 0 <= col < 3) or self.board[row, col] != 0:
            return False
        
        self.board[row, col] = self.current_player
        self._check_game_over()
        self.current_player = -self.current_player
        return True
    
    def _check_game_over(self) -> None:
        """Check if the game is over and set winner if applicable."""
        # Check rows, columns and diagonals
        for i in range(3):
            # Check rows
            if abs(sum(self.board[i, :])) == 3:
                self.game_over = True
                self.winner = self.board[i, 0]
                return
            # Check columns
            if abs(sum(self.board[:, i])) == 3:
                self.game_over = True
                self.winner = self.board[0, i]
                return
        
        # Check diagonals
        if abs(sum(np.diag(self.board))) == 3:
            self.game_over = True
            self.winner = self.board[0, 0]
            return
        if abs(sum(np.diag(np.fliplr(self.board)))) == 3:
            self.game_over = True
            self.winner = self.board[0, 2]
            return
        
        # Check for draw
        if np.all(self.board != 0):
            self.game_over = True
            self.winner = 0
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Return list of valid moves as (row, col) tuples."""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]
    
    def get_state(self) -> np.ndarray:
        """Return current game state as a numpy array."""
        return self.board.copy()
    
    def is_terminal(self) -> bool:
        """Check if the current state is a terminal state."""
        return self.game_over
    
    def get_reward(self) -> Optional[float]:
        """Return reward for the current state. None if game is not over."""
        if not self.game_over:
            return None
        if self.winner == 0:
            return 0.0  # Draw
        return 1.0 if self.winner == 1 else -1.0
    
    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
    
    def __str__(self) -> str:
        """String representation of the game board."""
        symbols = {0: ' ', 1: 'X', -1: 'O'}
        board_str = ''
        for i in range(3):
            board_str += '|'
            for j in range(3):
                board_str += f' {symbols[self.board[i, j]]} |'
            board_str += '\n'
            if i < 2:
                board_str += '|---|---|---|\n'
        return board_str

# Example usage
if __name__ == "__main__":
    game = TicTacToe()
    print("Initial board:")
    print(game)
    
    # Example game
    moves = [(0, 0), (1, 1), (0, 1), (1, 2), (0, 2)]  # X wins
    for row, col in moves:
        game.make_move(row, col)
        print(f"\nAfter move ({row}, {col}):")
        print(game)
        if game.is_terminal():
            print(f"Game Over! Winner: {'X' if game.winner == 1 else 'O' if game.winner == -1 else 'Draw'}")
            break
