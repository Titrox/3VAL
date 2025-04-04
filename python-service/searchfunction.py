import validation
import logging

INFINITY = float('inf')
NEG_INFINITY = float('-inf')

counter = 0


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()


def MINIMAX(chessboard, depth, is_white, move):
    global counter
    counter += 1
    logger.debug(counter)

    logger.debug(f"MINMAX SEARCH: {counter}")
    logger.debug(chessboard)
    game_over, reason = validation.game_over(chessboard, is_white)

    if depth == 0 or game_over:
        logger.debug("Matt or Patt")
        if not game_over: # not Matt or Patt  
             return Move_with_value(move.start, move.end, validation.evaluate_position(chessboard))  # Bewertung der Stellung
        
        if is_white: # Matt or Patt and Maximizer
            return Move_with_value(move.start, move.end, INFINITY) if reason == 0 else Move_with_value(move.start, move.end, 0) 
        
        else: # Matt or Patt and Minimizer
            return Move_with_value(move.start, move.end, NEG_INFINITY) if reason == 0 else Move_with_value(move.start, move.end, 0)


    if is_white:  # Maximizer
        best_move = Move_with_value(0, 0, NEG_INFINITY)
        best_first_move = None  # Speichert den besten ersten Zug auf der höchsten Ebene

        for start, value in validation.generate_legal_moves(chessboard, is_white).items():
            for end in value:
                move = Move(start, end)
                new_board = validation.make_move(start, end, chessboard)
                new_move = MINIMAX(new_board, depth - 1, False, move)

                if new_move.value > best_move.value:
                    best_move = new_move
                    best_first_move = move  # Speichere den ersten Zug auf der obersten Ebene

        if best_first_move is None:  # Falls keine Züge möglich sind
            return best_move

        return Move_with_value(best_first_move.start, best_first_move.end, best_move.value)  # Gib den besten ersten Zug zurück

    else:  # Minimizer
        best_move = Move_with_value(0, 0, INFINITY)
        best_first_move = None  # Speichert den besten ersten Zug auf der höchsten Ebene

        for start, value in validation.generate_legal_moves(chessboard, is_white).items():
            for end in value:
                move = Move(start, end)
                new_board = validation.make_move(start, end, chessboard)
                new_move = MINIMAX(new_board, depth - 1, True, move)

                if new_move.value < best_move.value:
                    best_move = new_move
                    best_first_move = move  # Speichere den ersten Zug auf der obersten Ebene

        if best_first_move is None:  # Falls keine Züge möglich sind
            return best_move

        return Move_with_value(best_first_move.start, best_first_move.end, best_move.value)  # Gib den besten ersten Zug zurück

    


class Move:

     def __init__(self, start, end):
        self.start = start
        self.end = end


class Move_with_value(Move):

    def __init__(self, start, end, value):
        super().__init__(start, end)
        self.value = value


    def to_chess_notation(self, position):
        column, row = position
        file = chr(97 + row)  # x von 0-7 -> 'a'-'h'
        rank = str(8 - column)   # y von 0-7 -> '8'-'1'
        # return file + rank
        return f"{file}{rank}"


    def to_dict(self):
        # Übersetzen der start und end Koordinaten in Schachnotation
        start_chess_notation = self.to_chess_notation(self.start)
        end_chess_notation = self.to_chess_notation(self.end)
        
        return {"from": start_chess_notation, "to": end_chess_notation}    