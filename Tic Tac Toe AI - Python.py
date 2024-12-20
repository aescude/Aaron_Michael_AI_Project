#copy this into the terminal to run  code
#    python3 'Tic Tac Toe AI - Python.py'

# (c) 2024 Roland Labana
import random

# Defines the Player class, showing both human and AI players
class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, game):
        raise NotImplementedError("Subclass must implement abstract method")

# Defines the HumanPlayer class, this class allows the human player to make moves
class HumanPlayer(Player):
    def make_move(self, game):
        while True:
            try:
                #this promts the player to move in the spaces 0-8
                move = int(input(f"Enter your move for '{self.symbol}' (0-8): "))
                if game.is_valid_move(move):
                    game.make_move(move, self.symbol)
                    break
                else:
                    #If not valid move, let the player pick another space
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number.")

class AIPlayer(Player):
    def __init__(self, symbol, strategy):
        super().__init__(symbol)
         # The AI uses a specific strategy(this strategy) to determine its moves
        self.strategy = strategy

    def make_move(self, game):
        print(f"{self.symbol}'s AI is thinking...")
        move = self.strategy.determine_move(game)
        # Check if the move is valid and make it
        if game.is_valid_move(move):
            game.make_move(move, self.symbol)
        else:
            print(f"Error: Invalid move suggested by {self.symbol}'s AI. Defaulting to random move.")
            # If the AI wants to play an invalid move, pick a random valid move
            for i in range(9):
                if game.is_valid_move(i):
                    game.make_move(i, self.symbol)
                    break

class TicTacToe:
    def __init__(self, player1, player2):
        # Initialize the game with a blank board and two players
        self.board = [' ' for _ in range(9)]
        self.players = [player1, player2]

    def play(self):
         while True:
              # Loop through each player in the game
            for player in self.players:
                self.display_board()
                # Display the current state of the board
                player.make_move(self)
                if self.check_win(self.board):
                    # Check if the player has won
                    self.display_board()
                    print(f"{player.symbol} wins!")
                    return
                if self.is_board_full():
                    #Check if the board is full
                    self.display_board()
                    print("It's a draw!")
                    return

    def is_valid_move(self, move):
         # Check if a move is valid 
        return self.board[move] == ' ' and 0 <= move <= 8

    def make_move(self, move, symbol):
        # Makes a move on the board by placing the player's symbol in the chosen spot(X or O)
        self.board[move] = symbol

    def check_win(self, theBoard):
        # Define the winning conditions(Rows, Columns, and Diagnals)
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(theBoard[i] == symbol for i in combo) for symbol in ['X', 'O'] for combo in win_conditions)

    def is_board_full(self):
        #Checks if the board is full
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

class AaronMikeMinimax:
    def __init__(self, symbol):
        self.mysymbol = symbol
        if symbol == 'O':
            enemysymbol = 'X'
        else:
            enemysymbol = 'O'
        self.enemysymbol = enemysymbol

    def depthevalfunc(self, game):
        if (game.board[4] == self.mysymbol) and (game.board[8] == self.mysymbol or game.board[6] == self.mysymbol or game.board[0] == self.mysymbol or game.board[2] == self.mysymbol):
            return 1
        if (game.board[4] == self.enemysymbol) and (game.board[8] == self.enemysymbol or game.board[6] == self.enemysymbol or game.board[0] == self.enemysymbol or game.board[2] == self.enemysymbol):
            return -1
        else:
            return 0


    def minimax_evaluation (self, game, arewemaximizing, curdepth):
        maxdepth = 10 
        #change this number to whatever depth you want it to go to

        if game.check_win(game.board) == True:
            if arewemaximizing == False:
                return 1
            else:
                return -1
        elif game.is_board_full() == True:
            return 0
            
        if curdepth == maxdepth: #if we reach the maximum depth we're gonna to go to
            best_value = self.depthevalfunc(game)
            return best_value

        
        if arewemaximizing == True:
            best_value = -float('inf')
            for move in range(9):
                if game.is_valid_move(move):
                    game.board[move] = self.mysymbol
                    valueofmove = self.minimax_evaluation(game, False, curdepth+1)
                    game.board[move] = ' '
                    best_value = max(valueofmove, best_value)
            return best_value
        
        else:
            best_value = float('inf')
            for move in range(9):
                if game.is_valid_move(move):
                    game.board[move] = self.enemysymbol
                    valueofmove = self.minimax_evaluation(game, True, curdepth+1)
                    game.board[move] = ' '
                    best_value = min(valueofmove, best_value)
            return best_value

    def determine_move(self, game):
        best_value = -float('inf')
        best_move = None # Store the current best move for AI
        curdepth = 0


        #going through the spaces of the board/list indexes
        for move in range(9):
            if game.is_valid_move(move): # Check if space is empty
                game.board[move] = self.mysymbol  # Simulate AI move
                valueofmove = self.minimax_evaluation(game, False, curdepth)
                game.board[move] = ' '
                
                # If this move has a better value, update the best move
                if valueofmove > best_value:
                    best_value = valueofmove # Update the best value found so far
                    best_move = move # Update the best move to the current move

        # Return the board location of the best move for the AI (the list index)
        return best_move


if __name__ == "__main__":
    # Here you can decide how to initialize players
    player1 = HumanPlayer('X')
    # You can choose any AI class below:
    player2 = AIPlayer('O', AaronMikeMinimax('O'))  # Minimax AI
    #player2 = AIPlayer('O', AaronMikeAI())  # AaronMike AI
    #player2 = AIPlayer('O', RandomAI())    # Random AI
    #player2 = AIPlayer('O', SimpleAI())    # Simple AI
    game = TicTacToe(player1, player2)
    game.play()
