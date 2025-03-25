import numpy as np
from TicTacToeGame import TicTacToe
from MinimaxAgent import MinimaxAgent
from TicTacToeVisualizer import TicTacToeVisualizer
import os

class HumanVsAIGame:
    def __init__(self, human_player=1, visualize=True, output_dir="game_images"):
        """
        Initialize a game where a human plays against the AI.
        Args:
            human_player: 1 for X (goes first), -1 for O (goes second)
            visualize: Whether to create visualization images
            output_dir: Directory to save visualization images
        """
        self.game = TicTacToe()
        self.human_player = human_player
        self.ai_player = -human_player
        self.ai_agent = MinimaxAgent(player=self.ai_player)
        
        # Set up visualization if enabled
        self.visualize = visualize
        if visualize:
            self.visualizer = TicTacToeVisualizer(output_dir=output_dir)
            # Clear any existing images
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    if file.startswith("human_vs_ai_"):
                        os.remove(os.path.join(output_dir, file))
    
    def display_board(self):
        """Display the current game board in the console."""
        print(self.game)
    
    def get_human_move(self):
        """Get move from human player with input validation."""
        valid_move = False
        while not valid_move:
            try:
                move_input = input("Enter your move as 'row,col' (e.g., 0,0 for top-left): ")
                row, col = map(int, move_input.split(','))
                
                if not (0 <= row < 3 and 0 <= col < 3):
                    print("Invalid coordinates! Both row and column must be between 0 and 2.")
                    continue
                
                if self.game.board[row, col] != 0:
                    print("That position is already taken! Try again.")
                    continue
                
                valid_move = True
            except ValueError:
                print("Invalid input! Please enter row and column as numbers separated by a comma.")
        
        return row, col
    
    def save_game_state(self, move_number, player_symbol):
        """Save the current game state as an image."""
        if self.visualize:
            save_path = os.path.join(self.visualizer.output_dir, 
                                    f"human_vs_ai_{move_number}_{player_symbol}.png")
            self.visualizer.draw_board(self.game, 
                                      f"Move {move_number} ({player_symbol})", 
                                      save_path)
    
    def play_game(self):
        """Run the game loop for human vs. AI."""
        # Initialize
        move_number = 0
        print("\nWelcome to Tic Tac Toe vs. AI!")
        print("You are playing as", "X" if self.human_player == 1 else "O")
        print("Your opponent (AI) is playing as", "O" if self.human_player == 1 else "X")
        print("\nCoordinates are (row,col), starting from (0,0) at the top-left:")
        print("(0,0) | (0,1) | (0,2)")
        print("---------------------")
        print("(1,0) | (1,1) | (1,2)")
        print("---------------------")
        print("(2,0) | (2,1) | (2,2)")
        print("\nLet's begin!\n")
        
        # Save initial state
        if self.visualize:
            save_path = os.path.join(self.visualizer.output_dir, "human_vs_ai_initial.png")
            self.visualizer.draw_board(self.game, "Initial Board", save_path)
            print("Game states will be saved in the", self.visualizer.output_dir, "directory")
        
        self.display_board()
        
        # Game loop
        while not self.game.is_terminal():
            current_player = self.game.current_player
            
            if current_player == self.human_player:
                print("\nYour turn...")
                row, col = self.get_human_move()
                self.game.make_move(row, col)
                move_number += 1
                print(f"\nYour move: ({row}, {col})")
                self.save_game_state(move_number, "X" if self.human_player == 1 else "O")
            else:
                print("\nAI is thinking...")
                ai_move = self.ai_agent.get_move(self.game)
                self.game.make_move(ai_move[0], ai_move[1])
                move_number += 1
                print(f"\nAI move: ({ai_move[0]}, {ai_move[1]})")
                self.save_game_state(move_number, "O" if self.human_player == 1 else "X")
            
            self.display_board()
        
        # Game over
        if self.game.winner == self.human_player:
            result = "You win! Congratulations!"
        elif self.game.winner == self.ai_player:
            result = "AI wins! Better luck next time."
        else:
            result = "It's a draw!"
        
        print("\nGame Over!", result)
        
        # Save final state
        if self.visualize:
            save_path = os.path.join(self.visualizer.output_dir, "human_vs_ai_final.png")
            self.visualizer.draw_board(self.game, f"Final Result: {result}", save_path)

def play_again():
    """Ask if the player wants to play again."""
    while True:
        response = input("\nDo you want to play again? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def choose_player():
    """Let the player choose X or O."""
    while True:
        choice = input("Do you want to play as X (first) or O (second)? (x/o): ").strip().lower()
        if choice in ['x', 'X']:
            return 1
        elif choice in ['o', 'O']:
            return -1
        else:
            print("Please enter 'x' or 'o'.")

if __name__ == "__main__":
    print("=" * 50)
    print("Welcome to Tic Tac Toe vs. Minimax AI")
    print("=" * 50)
    
    playing = True
    while playing:
        human_player = choose_player()
        game = HumanVsAIGame(human_player=human_player)
        game.play_game()
        playing = play_again()
    
    print("\nThanks for playing! Goodbye!") 