import validation
import logging

# Define infinity values for minimax algorithm
INFINITY = float('inf')
NEG_INFINITY = float('-inf')

# Initialize a counter for debugging purposes
counter = 0

# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()

# Minimax algorithm implementation to find the best move
def MINIMAX(chessboard_object, depth, is_white, move):
    global counter
    counter += 1
    logger.debug(counter)

    chessboard = chessboard_object.chessboard

    logger.debug(f"MINMAX SEARCH: {counter}")
    logger.debug(chessboard)

    # Base case: if the maximum depth is reached
    if depth == 0:

        # Check if the game is over (checkmate or stalemate)
        game_over, reason = validation.game_over(chessboard_object, is_white)

        # If the game is not over, evaluate the current position
        if not game_over: # not Checkmate or Stalemate
            return Move_with_value(move.start, move.end, validation.evaluate_position(chessboard)) # Evaluate the position

        # If the game is over and it's the maximizer's turn (white)
        if is_white: # Checkmate or Stalemate and Maximizer
            return Move_with_value(move.start, move.end, INFINITY) if reason == 0 else Move_with_value(move.start, move.end, 0) # Return infinity for checkmate, 0 for stalemate

        # If the game is over and it's the minimizer's turn (black)
        else: # Checkmate or Stalemate and Minimizer
            return Move_with_value(move.start, move.end, NEG_INFINITY) if reason == 0 else Move_with_value(move.start, move.end, 0) # Return negative infinity for checkmate, 0 for stalemate

    # Maximizer's turn (white)
    if is_white:
        best_move = Move_with_value(0, 0, NEG_INFINITY)
        best_first_move = None # Stores the best first move at the highest level

        # Iterate through all legal moves
        for start, value in validation.generate_legal_moves(chessboard_object, is_white).items():
            for end in value:
                move = Move(start, end)
                # Simulate the move on a new chessboard object
                new_chessboard_object = validation.make_move(start, end, chessboard_object)
                # Recursively call MINIMAX for the opponent
                new_move = MINIMAX(new_chessboard_object, depth - 1, False, move)

                # Update the best move if a better one is found
                if new_move.value > best_move.value:
                    best_move = new_move
                    best_first_move = move # Store the first move at the top level

        # If no moves are possible
        if best_first_move is None:
            return best_move

        # Return the best first move found at the current level
        return Move_with_value(best_first_move.start, best_first_move.end, best_move.value)

    # Minimizer's turn (black)
    else:
        best_move = Move_with_value(0, 0, INFINITY)
        best_first_move = None # Stores the best first move at the highest level

        # Iterate through all legal moves
        for start, value in validation.generate_legal_moves(chessboard_object, is_white).items():
            for end in value:
                move = Move(start, end)
                # Simulate the move on a new chessboard object
                new_chessboard_object = validation.make_move(start, end, chessboard_object)
                # Recursively call MINIMAX for the opponent
                new_move = MINIMAX(new_chessboard_object, depth - 1, True, move)

                # Update the best move if a better one is found
                if new_move.value < best_move.value:
                    best_move = new_move
                    best_first_move = move # Store the first move at the top level

        # If no moves are possible
        if best_first_move is None:
            return best_move

        # Return the best first move found at the current level
        return Move_with_value(best_first_move.start, best_first_move.end, best_move.value)


# Class to represent a chess move with start and end positions
class Move:

    def __init__(self, start, end):
        self.start = start
        self.end = end


# Class to represent a chess move with its associated evaluation value
class Move_with_value(Move):

    def __init__(self, start, end, value):
        super().__init__(start, end)
        self.value = value

    # Convert a board position (row, column) to chess notation (e.g., 'a1')
    def to_chess_notation(self, position):
        column, row = position
        file = chr(97 + row) # column from 0-7 -> 'a'-'h'
        rank = str(8 - column)  # row from 0-7 -> '8'-'1'
        return f"{file}{rank}"

    # Convert the Move_with_value object to a dictionary with chess notation
    def to_dict(self):
        # Translate the start and end coordinates to chess notation
        start_chess_notation = self.to_chess_notation(self.start)
        end_chess_notation = self.to_chess_notation(self.end)

        return {
            "move": {
                "from": start_chess_notation, "to": end_chess_notation
                },
            "value" : str(self.value) if self.value in (float('inf'), float('-inf')) else self.value
            }
    