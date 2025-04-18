import validation
import logging
import time

# Define infinity values for minimax algorithm
INFINITY = float('inf')
NEG_INFINITY = float('-inf')

# Initialize a counter for debugging purposes
counter = 0


# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()



# Minimax algorithm implementation to find the best move
def MINIMAX(chessboard_object, depth, max_depth, is_white, move_leading_here, alpha, beta):
    global counter
    counter += 1
    logger.debug(counter)

    
    chessboard = chessboard_object.chessboard

    # BASE CASES

    game_over, reason = validation.game_over(chessboard_object, is_white)

    if game_over:
        
        if reason == 0:  # Checkmate
            value = NEG_INFINITY if is_white else INFINITY
        else:  # Stalemate
            value = 0


        return Move_with_value(move_leading_here.start, move_leading_here.end, value, None)
    

    if depth == max_depth:  # Max search depth reached

        best_moves_per_depth
        return Move_with_value(move_leading_here.start, move_leading_here.end,
                                 validation.evaluate_position(chessboard),
                                 chessboard_object.promotion)
    
    if is_white:  # Maximizing player (White)

        best_move = Move_with_value(None, None, NEG_INFINITY, None)
        legal_moves = validation.generate_legal_moves(chessboard_object, is_white)

        
        ordered_moves = order_moves(chessboard_object, legal_moves, is_white)
        


        for move in ordered_moves:

            new_chessboard_object = validation.make_move(move.start, move.end, chessboard_object)
            current_promotion = new_chessboard_object.promotion
            action_taken = Move(move.start, move.end)

            result = MINIMAX(new_chessboard_object, depth + 1, max_depth, not is_white, action_taken, alpha, beta)

            best_moves_per_depth.setdefault(depth,[]).extend((move.start, move.end, result.value)) # Store move in dic for iterative deepening

            if result.value > best_move.value:
                best_move = Move_with_value(move.start, move.end, result.value, current_promotion)

            alpha = max(alpha, result.value)

            if beta <= alpha:
                logger.debug(f"White pruned at depth {depth}, alpha={alpha}, beta={beta}")
                return best_move  # Prune: Stop searching further down this path

        return best_move

    else:  # Minimizing player (Black)
        
        best_move = Move_with_value(None, None, INFINITY, None)
        legal_moves = validation.generate_legal_moves(chessboard_object, is_white)

        ordered_moves = order_moves(chessboard_object, legal_moves, is_white)
        


        for move in ordered_moves:

            new_chessboard_object = validation.make_move(move.start, move.end, chessboard_object)
            current_promotion = new_chessboard_object.promotion
            action_taken = Move(move.start, move.end)

            result = MINIMAX(new_chessboard_object, depth + 1, max_depth, not is_white, action_taken, alpha, beta)

            if result.value < best_move.value:
                best_move = Move_with_value(move.start, move.end, result.value, current_promotion)

            beta = min(beta, result.value)

            if beta <= alpha:
                logger.debug(f"White pruned at depth {depth}, alpha={alpha}, beta={beta}")
                return best_move  # Prune: Stop searching further down this path

        return best_move




def iterative_deepening(chessboard_object, is_white, max_time=2.0):
    start_time = time.time()
    time_limit = start_time + max_time

    best_move = None
    max_depth = 0

    while True:
        current_time = time.time()
        if current_time >= time_limit:
            break

    
        logger.debug(f"NEW ITERATIVE DEEPENING ITERATION, MAX_DEPTH = {max_depth}")
        # Optional: add a timeout checker inside search
        move = MINIMAX(chessboard_object, 0, max_depth, is_white, Move(0,0), NEG_INFINITY, INFINITY)
        logger.debug("MAX DEPTH - 1 BEST MOVES")
        logger.debug(best_moves_per_depth.get(max_depth - 1))

      
        best_moves_per_depth.clear()

            
        if move:
            best_move = move
        max_depth += 1



    return best_move


def order_moves(chessboard_object, legal_moves, is_white):
    
    sorted_moves = quicksort(moves_to_array(chessboard_object, legal_moves), is_white)  # Calls moves_to_array and then quicksort
    return sorted_moves


def moves_to_array(chessboard_object, legal_moves):

    all_moves = []
    for start, value_list in legal_moves.items():
        for end in value_list:
            move_object = Move_with_value(start, end, get_move_value(start, end, chessboard_object), None)
            all_moves.append(move_object)
    
    
    return all_moves



# Returns the value of a given move
def get_move_value(start, end, chessboard_object):
    
    sim = validation.make_move(start, end, chessboard_object)  # Simulates the move
    return validation.calc_piece_value_with_psqt(sim.chessboard)  # Calculates the heuristic value



#
# QUICKSORT
#

def quicksort(array, is_white, low=0, high=None):
 
    if high is None:
        high = len(array) - 1

    if low < high:
        pivot_index = partition(array, low, high, is_white)  # Partitions the array
        quicksort(array, is_white, low, pivot_index - 1)  # Sorts the left partition
        quicksort(array, is_white, pivot_index + 1, high)  # Sorts the right partition
    
    return array




def partition(array, low, high, is_white):
  
    pivot = array[high].value  # Chooses the last element as the pivot
    i = low - 1

    for j in range(low, high):

        if not is_white: # Sort ascending for Minimizer (Black)

            if array[j].value <= pivot:
                i += 1
                array[i], array[j] = array[j], array[i]  # Swaps elements

        else:  # Sort descending for Minimizer (Black)

            if array[j].value >= pivot:
                i += 1
                array[i], array[j] = array[j], array[i]  # Swaps elements

    array[i + 1], array[high] = array[high], array[i + 1]  # Swaps pivot
    return i + 1  # Returns the new index of the pivot





#
# CLASSES
#


    

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
