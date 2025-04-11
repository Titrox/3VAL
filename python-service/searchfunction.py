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
def MINIMAX(chessboard_object, depth, is_white, move_leading_here): 
    global counter
    counter += 1
    logger.debug(counter)

    chessboard = chessboard_object.chessboard

    # BASECASES
    game_over, reason = validation.game_over(chessboard_object, is_white)
    if game_over:

        if reason == 0: # Checkmate
            
            value = INFINITY if is_white else NEG_INFINITY

        else: # Patt
            value = 0 
        
        # Return move
        return Move_with_value(move_leading_here.start, move_leading_here.end, value, None)

    if depth == 0: # Max depth reached

        # return evaluated chessboard
        return Move_with_value(move_leading_here.start, move_leading_here.end,
                               validation.evaluate_position(chessboard),
                               chessboard_object.promotion)


    if is_white: # Maximizer
        
        # Initialise best move at this recursion level
        best_move_at_this_level = Move_with_value(None, None, NEG_INFINITY, None)

        # Iterate trough all legal moves 
        for start, value_list in validation.generate_legal_moves(chessboard_object, is_white).items():
            for end in value_list:

                # Simulating move
                new_chessboard_object = validation.make_move(start, end, chessboard_object)

                # Move was a pawn pormotion?
                current_promotion = new_chessboard_object.promotion


                action_taken = Move(start, end)

                # Recursive call (Minimizer - Black)
                recursive_result = MINIMAX(new_chessboard_object, depth - 1, False, action_taken)

                # Update best possible move on this 
                if recursive_result.value > best_move_at_this_level.value:
                    
                    best_move_at_this_level = Move_with_value(start, end, recursive_result.value, current_promotion)

        # Gib den besten auf dieser Ebene gefundenen Zug zurück
        return best_move_at_this_level

    else: # Minimierer (Schwarz)
        # Initialisiere den besten Zug auf dieser Ebene mit dem schlechtesten Wert für Schwarz
        best_move_at_this_level = Move_with_value(None, None, INFINITY, None)

        # Iteriere durch alle legalen Züge für Schwarz aus der aktuellen Position
        # ACHTUNG: Hier muss is_white (also False) an generate_legal_moves übergeben werden!
        for start, value_list in validation.generate_legal_moves(chessboard_object, is_white).items(): # is_white ist hier False
            for end in value_list:
                # Simuliere den Zug
                new_chessboard_object = validation.make_move(start, end, chessboard_object)
                # Hole die Promotion-Info NACH dem Zug vom neuen Brett-Objekt
                current_promotion = new_chessboard_object.promotion

                # Erstelle ein einfaches Objekt für den gerade ausgeführten Zug
                action_taken = Move(start, end)

                # Rekursiver Aufruf für den Gegner (Weiß)
                recursive_result = MINIMAX(new_chessboard_object, depth - 1, True, action_taken)

                # Vergleiche den Wert aus der Rekursion mit dem bisher besten Wert
                if recursive_result.value < best_move_at_this_level.value:
                    # Update: Speichere den Zug DIESER Ebene (start, end),
                    # den Wert aus der Rekursion (recursive_result.value),
                    # und die Promotion DIESES Zuges (current_promotion).
                    best_move_at_this_level = Move_with_value(start, end, recursive_result.value, current_promotion)

        # Gib den besten auf dieser Ebene gefundenen Zug zurück
        return best_move_at_this_level


# Class to represent a chess move with start and end positions
class Move:
    def __init__(self, start, end):
        self.start = start # Erwartet Tupel (row_idx, col_idx)
        self.end = end     # Erwartet Tupel (row_idx, col_idx)


# Class to represent a chess move with its associated evaluation value and promotion
class Move_with_value(Move):
    def __init__(self, start, end, value, promotion):
        super().__init__(start, end)
        self.value = value
        self.promotion = promotion # Soll 'q', 'r', 'n', 'b' oder None sein

    # --- Methoden to_chess_notation und to_dict bleiben wie zuvor ---
    def to_chess_notation(self, position):
        if position is None: # Sicherheitscheck für Initialisierung
             return None
        column, row = position
        file = chr(97 + row)
        rank = str(8 - column)
        return f"{file}{rank}"

    def to_dict(self):
         # Translate the start and end coordinates to chess notation
         start_chess_notation = self.to_chess_notation(self.start)
         end_chess_notation = self.to_chess_notation(self.end)

         # Erstelle das innere Dictionary für den Zug
         move_data = {
             "from": start_chess_notation,
             "to": end_chess_notation
         }

         # Füge Promotion hinzu, wenn vorhanden
         if self.promotion is not None:
             move_data["promotion"] = self.promotion

         # Erstelle das finale Dictionary
         result_dict = {
             "move": move_data,
             "value": str(self.value) if self.value in (float('inf'), float('-inf')) else self.value
         }

         # Korrektur: Das vorherige "promotion" wurde fälschlicherweise außerhalb von "move" hinzugefügt.
         # Die Logik oben fügt es korrekt in move_data ein.
         return result_dict