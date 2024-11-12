#copy this into the terminal to run  code
#    python3 'Tic Tac Toe AI - Python.py'

# (c) 2024 Roland Labana
import random

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, game):
        raise NotImplementedError("Subclass must implement abstract method")

class HumanPlayer(Player):
    def make_move(self, game):
        while True:
            try:
                move = int(input(f"Enter your move for '{self.symbol}' (0-8): "))
                if game.is_valid_move(move):
                    game.make_move(move, self.symbol)
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number.")

class AIPlayer(Player):
    def __init__(self, symbol, strategy):
        super().__init__(symbol)
        self.strategy = strategy

    def make_move(self, game):
        print(f"{self.symbol}'s AI is thinking...")
        move = self.strategy.determine_move(game)
        if game.is_valid_move(move):
            game.make_move(move, self.symbol)
        else:
            print(f"Error: Invalid move suggested by {self.symbol}'s AI. Defaulting to random move.")
            for i in range(9):
                if game.is_valid_move(i):
                    game.make_move(i, self.symbol)
                    break

class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [' ' for _ in range(9)]
        self.players = [player1, player2]

    def play(self):
         while True:
            for player in self.players:
                self.display_board()
                player.make_move(self)
                if self.check_win(self.board):
                    self.display_board()
                    print(f"{player.symbol} wins!")
                    return
                if self.is_board_full():
                    self.display_board()
                    print("It's a draw!")
                    return

    def is_valid_move(self, move):
        return self.board[move] == ' ' and 0 <= move <= 8

    def make_move(self, move, symbol):
        self.board[move] = symbol

    def check_win(self, theBoard):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(theBoard[i] == symbol for i in combo) for symbol in ['X', 'O'] for combo in win_conditions)

    def is_board_full(self):
        return ' ' not in self.board

    def display_board(self):
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("-----------")
        print()

# Example AI strategies

# Simple AI - pick FIRST available space 0 - 8
class SimpleAI:
    def determine_move(self, game):
        # Simple strategy: check for winning move, then blocking opponent's win, then take first open space
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'X'  # Assuming this AI plays 'X'
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'O'  # Check if opponent ('O') could win
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check
        # If no immediate winning or blocking move, take first available space
        for i in range(9):
            if game.is_valid_move(i):
                return i

# Random AI - pick a RANDOM available space 0 - 8
class RandomAI:
    def determine_move(self, game):
        possibleMoves = []
        # Add all open spaces into a list to then randomly choose one
        for i in range(9):
            if game.is_valid_move(i):
                possibleMoves.append(i)
        return random.choice(possibleMoves)

class AaronAI:
    def determine_move(self, game):
        possibleMoves = []
        # Add all open spaces into a list to then randomly choose one
        for i in range(9):
            if game.is_valid_move(i):
                possibleMoves.append(i)

        if 4 in possibleMoves:
            pickedmove = 4
        else:
            pickedmove = random.choice(possibleMoves)
        return pickedmove

class AaronMikeAI:
    def determine_move(self, game):
        possibleMoves = []
        # Add all open spaces into a list called possibleMoves
        for i in range(9):
            if game.is_valid_move(i):
                possibleMoves.append(i)

        # Check if we have a winning move
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'O'  # Assuming the AI plays O
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    # Returns move we need to win
                    return i
                game.board[i] = ' '  # Reset for next check

        # Check if the enemy has a winning move
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'X'  # Check if opponent X could win
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    # Returns move we need to block opponent, basically their winning move
                    return i
                game.board[i] = ' '  # Reset for next check

        # Placing in the middle as first choice if no winning or blocking moves are available
        if 4 in possibleMoves:
            return 4

        # Placing in the corners if no middle or winning or blocking moves are available
        # Goes through list of corners, checks if any are available moves, and then places first available corner
        for corneroption in [0, 2, 6, 8]:
            if corneroption in possibleMoves:
                return corneroption

        # If no corners or middle or winning or blocking moves are available, place in a random available space
        return random.choice(possibleMoves)

#class for the node used in the minimax
class MinimaxNode:
    # Creating the node template with board info, which player it is (X or O), its value once it gets given one, and its children if it has any
    def __init__(self, board, player):
        self.board = board[:] # Make a copy of the board to avoid modifying the original
        self.player = player # Store the current player
        self.value = None # Value to store the result of the minimax evaluation (initialized as None)
        self.children = [] # List to store child nodes (next possible game states)

    # Checking if the board is in a terminal state (X or O has won, or all spaces filled)
    def is_terminal(self):
        return self.check_win('X') or self.check_win('O') or ' ' not in self.board

    # Rewriting check win function since we arent working with game class in this area, also so that we can actually get which symbol won
    def check_win(self, board):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(board[i] == symbol for i in combo) for symbol in ['X', 'O'] for combo in win_conditions)

    def generate_children(self):
        # If in terminal state, no children needed
        if self.is_terminal():
            return []
        children = []
        # Loop through board positions and generate possible moves
        for i in range(9):
            if self.board[i] == ' ': # Only generate moves for empty spaces
                new_board = self.board[:] # Make a copy of the current board
                new_board[i] = self.player # Make the move for the current player
                new_player = 'O' if self.player == 'X' else 'X'  # Switch to the opponent's turn
                
                # Create a new node (child) with the updated board and the opponent as the next player
                children.append(MinimaxNode(new_board, new_player))
        return children

    def minimax(self):
        # Setting the values once terminal state is hit
        if self.is_terminal():
            if self.check_win('X'):
                return 1  # X wins
            elif self.check_win('O'):
                return -1  # O wins
            else:
                return 0  # Tie

        # Generate possible children nodes
        children = self.generate_children()
        if self.player == 'X':  # Maximizing player
            return max(child.minimax() for child in children)
        else:  # Minimizing player
            return min(child.minimax() for child in children)

class MinimaxAI:
    def determine_move(self, game):
        best_value = float('-inf') # Start with lowest value since X is maximizing
        best_move = -1 # Store the best move

        for i in range(9):
            if game.is_valid_move(i): # Check if space is empty
                game.board[i] = 'O'  # Simulate AI O move
                node = MinimaxNode(game.board, 'X') # Change turns
                move_value = node.minimax() # Calculate the value of this move
                game.board[i] = ' '  # Reset

                # If this move has a better value, update the best move
                if move_value > best_value:
                    best_value = move_value # Update the best value found so far
                    best_move = i # Update the best move to the current move i

        # Return the board location of the best move for the AI
        return best_move

if __name__ == "__main__":
    # Here you can decide how to initialize players
    player1 = HumanPlayer('X')
    # You can choose any AI class below:
    player2 = AIPlayer('O', MinimaxAI())  # Minimax AI
    #player2 = AIPlayer('O', AaronMikeAI())  # AaronMike AI
    #player2 = AIPlayer('O', RandomAI())    # Random AI
    #player2 = AIPlayer('O', SimpleAI())    # Simple AI
    game = TicTacToe(player1, player2)
    game.play()
