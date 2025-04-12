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
def MINIMAX(chessboard_object, depth, is_white, move_leading_here, alpha, beta):
    global counter
    counter += 1
    logger.debug(counter)

    chessboard = chessboard_object.chessboard

    # BASE CASES
    game_over, reason = validation.game_over(chessboard_object, is_white)
    if game_over:
        if reason == 0:  # Checkmate
            value = INFINITY if is_white else NEG_INFINITY
        else:  # Stalemate
            value = 0
        return Move_with_value(move_leading_here.start, move_leading_here.end, value, None)

    if depth == 0:  # Max search depth reached
        return Move_with_value(move_leading_here.start, move_leading_here.end,
                                 validation.evaluate_position(chessboard),
                                 chessboard_object.promotion)

    if is_white:  # Maximizing player (White)
        best_move = Move_with_value(None, None, NEG_INFINITY, None)
        legal_moves = validation.generate_legal_moves(chessboard_object, is_white)

        for start, value_list in legal_moves.items():
            for end in value_list:
                new_chessboard_object = validation.make_move(start, end, chessboard_object)
                current_promotion = new_chessboard_object.promotion
                action_taken = Move(start, end)

                result = MINIMAX(new_chessboard_object, depth - 1, not is_white, action_taken, alpha, beta)

                if result.value > best_move.value:
                    best_move = Move_with_value(start, end, result.value, current_promotion)

                alpha = max(alpha, result.value)

                if beta <= alpha:
                    logger.debug(f"White pruned at depth {depth}, alpha={alpha}, beta={beta}")
                    return best_move  # Prune: Stop searching further down this path

        return best_move

    else:  # Minimizing player (Black)
        best_move = Move_with_value(None, None, INFINITY, None)
        legal_moves = validation.generate_legal_moves(chessboard_object, False) # Corrected: is_white to False

        for start, value_list in legal_moves.items():
            for end in value_list:
                new_chessboard_object = validation.make_move(start, end, chessboard_object)
                current_promotion = new_chessboard_object.promotion
                action_taken = Move(start, end)

                result = MINIMAX(new_chessboard_object, depth - 1, not is_white, action_taken, alpha, beta)

                if result.value < best_move.value:
                    best_move = Move_with_value(start, end, result.value, current_promotion)

                beta = min(beta, result.value) # Corrected beta update

                if beta <= alpha:
                    logger.debug(f"Black pruned at depth {depth}, alpha={alpha}, beta={beta}")
                    return best_move  # Prune: Stop searching further down this path

        return best_move


# Class to represent a basic chess move (start and end positions)
class Move:
    def __init__(self, start, end):
        self.start = start  # Tuple (row_idx, col_idx)
        self.end = end      # Tuple (row_idx, col_idx)


# Move with additional value (evaluation) and promotion info
class Move_with_value(Move):
    def __init__(self, start, end, value, promotion):
        super().__init__(start, end)
        self.value = value
        self.promotion = promotion  # currently only 'q',

    def to_chess_notation(self, position):
        if position is None:
            return None
        column, row = position
        file = chr(97 + row)
        rank = str(8 - column)
        return f"{file}{rank}"

    def to_dict(self):
        start_notation = self.to_chess_notation(self.start)
        end_notation = self.to_chess_notation(self.end)

        move_data = {
            "from": start_notation,
            "to": end_notation
        }

        if self.promotion is not None:
            move_data["promotion"] = self.promotion

        return {
            "move": move_data,
            "value": str(self.value) if self.value in (float('inf'), float('-inf')) else self.value
        }
