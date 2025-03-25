import matplotlib.pyplot as plt
import numpy as np
import os
from typing import List, Tuple, Dict
from TicTacToeGame import TicTacToe
from MinimaxAgent import MinimaxAgent

class TicTacToeVisualizer:
    def __init__(self, output_dir="game_images"):
        """
        Initialize the visualizer with matplotlib settings.
        Args:
            output_dir: Directory to save image files
        """
        plt.style.use('ggplot')  # Using ggplot style which is built-in
        self.colors = {
            1: '#FF6B6B',  # Red for X
            -1: '#4ECDC4',  # Teal for O
            0: '#F7F7F7'   # Light gray for empty
        }
        self.output_dir = output_dir
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
    def draw_board(self, game: TicTacToe, title: str = "Tic Tac Toe", 
                   save_path: str = None):
        """
        Draw the current game board.
        Args:
            game: Current TicTacToe game instance
            title: Title for the plot
            save_path: Path to save the image to
        """
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title(title, pad=20)
        
        # Draw grid
        for i in range(4):
            ax.axhline(y=i, color='black', linewidth=2)
            ax.axvline(x=i, color='black', linewidth=2)
        
        # Draw X's and O's
        for i in range(3):
            for j in range(3):
                if game.board[i, j] != 0:
                    if game.board[i, j] == 1:  # X
                        ax.plot([j+0.2, j+0.8], [2-i+0.2, 2-i+0.8], 
                               color=self.colors[1], linewidth=3)
                        ax.plot([j+0.2, j+0.8], [2-i+0.8, 2-i+0.2], 
                               color=self.colors[1], linewidth=3)
                    else:  # O
                        circle = plt.Circle((j+0.5, 2-i+0.5), 0.3, 
                                          fill=False, color=self.colors[-1], linewidth=3)
                        ax.add_patch(circle)
        
        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(-0.5, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout()
        
        # Save the figure if a path is provided
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        plt.close(fig)
        return fig, ax
    
    def visualize_game(self, game: TicTacToe, moves: List[Tuple[int, int]]):
        """
        Visualize a sequence of moves in the game, saving each state as an image.
        Args:
            game: TicTacToe game instance
            moves: List of moves to visualize
        """
        game.reset()
        for i, move in enumerate(moves):
            game.make_move(move[0], move[1])
            save_path = os.path.join(self.output_dir, f"move_{i+1}.png")
            self.draw_board(game, f"Move {i+1}", save_path)
            print(f"Saved game state after move {i+1} to {save_path}")
    
    def visualize_minimax_game(self):
        """
        Visualize a complete game between two minimax agents, saving each state.
        """
        game = TicTacToe()
        x_agent = MinimaxAgent(player=1)
        o_agent = MinimaxAgent(player=-1)
        
        # Save initial state
        initial_path = os.path.join(self.output_dir, "initial_state.png")
        self.draw_board(game, "Initial State", initial_path)
        print(f"Saved initial game state to {initial_path}")
        
        moves = []
        move_count = 0
        while not game.is_terminal():
            current_agent = x_agent if game.current_player == 1 else o_agent
            move = current_agent.get_move(game)
            moves.append(move)
            game.make_move(move[0], move[1])
            
            # Save state after each move
            move_count += 1
            player_symbol = "X" if game.current_player == -1 else "O"  # Player who just moved
            save_path = os.path.join(self.output_dir, f"move_{move_count}_{player_symbol}.png")
            self.draw_board(game, f"After Move {move_count} ({player_symbol})", save_path)
            print(f"Saved game state after move {move_count} to {save_path}")
        
        # Save final state
        final_path = os.path.join(self.output_dir, "final_state.png")
        winner = "X" if game.winner == 1 else "O" if game.winner == -1 else "Draw"
        self.draw_board(game, f"Final State: {winner}", final_path)
        print(f"Saved final game state to {final_path}")
        
        print(f"\nGame Over! Winner: {winner}")
        print(f"All game states have been saved to the '{self.output_dir}' directory")

# Example usage
if __name__ == "__main__":
    # Create visualizer
    visualizer = TicTacToeVisualizer(output_dir="game_images")
    
    # Visualize a complete game between minimax agents
    print("Starting visualization of a game between minimax agents...")
    visualizer.visualize_minimax_game()
    
    # Example of visualizing a specific game state
    game = TicTacToe()
    game.make_move(0, 0)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 1)  # X
    
    save_path = os.path.join(visualizer.output_dir, "example_state.png")
    visualizer.draw_board(game, "Example Game State", save_path)
    print(f"Saved example game state to {save_path}") 