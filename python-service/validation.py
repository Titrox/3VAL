from flask import Flask, request
import urllib.parse
import logging
import constants
import searchfunction
import copy
import json


# Setting up basic logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()

# Initialize Flask application
app = Flask(__name__)

Pieces = constants.Pieces

# Flask route to get the best move using the minimax algorithm
# Returns a dictionary with 'from' and 'to' fields
@app.route('/best-move', methods=['POST'])
def get_best_move():
        
    data = request.get_json()

    is_white = data["is_white"]  # Boolean indicating if it's white's turn

    received_fen = data["fen"]  # Get the FEN string from the request
    formatted_fen = urllib.parse.unquote(received_fen)  # Decode URL-encoded FEN string to ASCII


    chessboard_object = fen_to_chessboard_object(formatted_fen)  # Convert FEN to chessboard object
    
    logger.debug(chessboard_object.chessboard)

    searchfunction.counter = 0  # Reset search counter

    # Search for the best move with depth 2
    best_move = searchfunction.MINIMAX(chessboard_object, 2, is_white, searchfunction.Move(0,0))
    logger.debug(best_move.to_dict)

    fen_to_chessboard_object(formatted_fen)

    return best_move.to_dict()  # Return the best move found


# Evaluates current chessboard position
def evaluate_position(chessboard):

    value = 0
    value += calc_piece_value_with_psqt(chessboard)  # Calculate value based on pieces and their positions

    return value


# Convert FEN string to a chessboard object
def fen_to_chessboard_object(fen):
    
    # Split FEN into board position and game information
    chessboard_fen, information_fen = fen.split(" ",1) 
    chessboard = fen_to_array(chessboard_fen)  # Convert the position part to a 2D array

    # Extract additional information from FEN
    turn_right, castling, en_passant, halfmove, fullmove = information_fen.split(" ")

    # Create a chessboard state object with the position and castling/en passant rights
    chessboard_object = Chessboard_state(chessboard, castling, en_passant)

    logger.debug(chessboard)
    # logger.debug(f"Turn: {chessboard_object.turn_right}, Castling: {chessboard_object.castling}, En Passant: {chessboard_object.en_passant}, Halfmove: {chessboard_object.halfmove}, Fullmove: {chessboard_object.fullmove}")

    return chessboard_object


# Convert FEN position string into a 2D array
def fen_to_array(fen):
    
    # Create empty 8x8 chessboard
    chessboard = [[0 for _ in range(8)] for _ in range(8)]

    current_field = 0
    current_row = 0
    current_column = 0

    # Process each character in the FEN string
    for char in fen: 

        if char.isalpha():  # If it's a piece
            current_row = current_field // 8
            current_column = current_field % 8
            chessboard[current_row][current_column] = char  # Place the piece on the board
            current_field += 1
           
        elif char.isdigit():  # If it's a number (empty squares)
            current_field += int(char)

        elif char == " ":  # End of the board position part
            break

    return chessboard


# Calculate the total value of a position based on piece values and piece-square tables
def calc_piece_value_with_psqt(chessboard):

    value = 0
    currentField = 0

    # Iterate through the 2D array
    for i in range(8): 
        for j in range(8): 

            char = chessboard[i][j]

            if char == 0:  # Empty square
                currentField += 1

            elif char.isupper():  # White piece
                psqtValue = get_psqt_value(currentField, char, True)  # Get position value
                value += getattr(Pieces, char, 0) + psqtValue  # Add piece value and position value

                currentField += 1 

            elif char.islower():  # Black piece
                psqtValue = get_psqt_value(currentField, char, False)  # Get position value
                value -= getattr(Pieces, char.upper(), 0) + psqtValue  # Subtract piece value and position value
            
                currentField += 1
   
    return value


# Get the position value from the piece-square table for a given piece and position
def get_psqt_value(field, piece, is_white):

    psqt = get_psqt_table(piece, is_white)  # Get the appropriate piece-square table
    kingOrQueen = piece.upper() == "K" or piece.upper() == "Q"
        
    # For black pieces or kings/queens, use the mirrored square value
    if not is_white or kingOrQueen:
        return psqt[63 - field]  # Return mirrored value
    else:
         return psqt[field]  # Return normal value
        

# Return the appropriate piece-square table for a given piece
def get_psqt_table(piece, is_white):
    
    match piece.upper():
        case 'P': return constants.Psqt.PAWN_PSQT
        case 'R': return constants.Psqt.ROOK_PSQT
        case 'B': return constants.Psqt.BISHOP_PSQT
        case 'N': return constants.Psqt.KNIGHT_PSQT
        case 'Q': return get_queen_psqt(is_white)
        case 'K': return get_king_psqt(is_white)
        case _: logger.error(f"no PSQT found for {piece}"); return -1  


# Return the appropriate king piece-square table based on color
def get_king_psqt(is_white):
    if is_white:
        return constants.Psqt.KING_PSQT
    else:
        return constants.Psqt.KING_PSQT_BLACK


# Return the appropriate queen piece-square table based on color
def get_queen_psqt(is_white):
    if is_white:
        return constants.Psqt.QUEEN_PSQT
    else:
        return constants.Psqt.QUEEN_PSQT_BLACK


# Generate all possible moves for each piece of the given color
def generate_moves(chessboard, is_white):
    
    moves = {}  # Dictionary to store moves: {(row, col): [(to_row, to_col), ...]}

    # Iterate through all positions on the board
    for i in range(8):
        for j in range(8):

            piece = chessboard[i][j]

            if piece == 0:  # Skip empty squares
                continue
                
            # Generate moves for white pieces if it's white's turn
            if piece.isupper() and is_white:

                match piece:
                    case 'P': moves.setdefault((i, j),[]).extend(pawn_moves(i, j, True, chessboard))
                    case 'B': moves.setdefault((i, j),[]).extend(bishop_moves(i, j, True, chessboard))
                    case 'N': moves.setdefault((i, j),[]).extend(knight_moves(i, j, True, chessboard))
                    case 'R': moves.setdefault((i, j),[]).extend(rook_moves(i,  j, True, chessboard))
                    case 'Q': moves.setdefault((i, j),[]).extend(queen_moves(i, j, True, chessboard))
                    case 'K': moves.setdefault((i, j),[]).extend(king_moves(i, j, True, chessboard))

            # Generate moves for black pieces if it's black's turn
            elif piece.islower() and not is_white: 

                match piece:
                    case 'p': moves.setdefault((i, j),[]).extend(pawn_moves(i, j, False, chessboard))
                    case 'b': moves.setdefault((i, j),[]).extend(bishop_moves(i, j, False, chessboard))
                    case 'n': moves.setdefault((i, j),[]).extend(knight_moves(i, j, False, chessboard))
                    case 'r': moves.setdefault((i, j),[]).extend(rook_moves(i, j, False, chessboard))
                    case 'q': moves.setdefault((i, j),[]).extend(queen_moves(i, j, False, chessboard))
                    case 'k': moves.setdefault((i, j),[]).extend(king_moves(i, j, False, chessboard))

    return moves
     

# Generate all legal moves (considering check)
def generate_legal_moves(chessboard_object, is_white):

    chessboard = chessboard_object.chessboard

    # Get legal castling moves if available
    castling_moves = legal_castling_moves(chessboard_object.castling, chessboard_object.chessboard, is_white)
    king_field = get_king_field(chessboard, is_white)  # Find the king's position
    
     # Get legal en passant moves if available
    en_passant_moves = legal_en_passant_moves(chessboard_object.en_passant, chessboard, is_white)
    logger.debug(f"En Passant: {en_passant_moves}")

    # Get all pseudo-legal moves
    all_moves = generate_moves(chessboard, is_white)
    legal_moves = {}

    # Filter out moves that would leave the king in check
    for key, value in all_moves.items():
        
        if (len(value) != 0):
           
            for move in value:
                # Simulate the move to see if it leaves the king in check
                sim_chessboard = make_move(key, move, chessboard_object).chessboard

                if not is_check(sim_chessboard, is_white): 
                    legal_moves.setdefault(key,[]).append((move[0], move[1]))  # Add legal move
                
    # Add castling moves if available
    if len(castling_moves) != 0:
        legal_moves.setdefault(king_field,[]).extend(castling_moves)

    if en_passant_moves:
        legal_moves.update(en_passant_moves)

    logger.debug(legal_moves)
    return legal_moves


# Check if castling is legal and return possible castling moves
def legal_castling_moves(possible_castling, chessboard, is_white):

    castling_moves = []
    
    if possible_castling == "-":  # No castling rights
        return castling_moves

    elif is_white:  # White castling

        if "Q" in possible_castling:  # Queenside castling
            # Check if squares between king and rook are empty
            Q_possible = chessboard[7][1] == 0 and chessboard[7][2] == 0 and chessboard[7][3] == 0  

            if Q_possible:
                sim_chessboard = copy.deepcopy(chessboard)  # Copy Chessboard

                # Simulate the castling move
                sim_chessboard[7][2] = 'K' 
                sim_chessboard[7][3] = 'R'

                # Check if castling would leave the king in check
                if not is_check(sim_chessboard, is_white):
                    castling_moves.append((7,2))

        if "K" in possible_castling:  # Kingside castling
            # Check if squares between king and rook are empty
            K_possible = chessboard[7][5] == 0 and chessboard[7][6] == 0 

            if K_possible:
                sim_chessboard = copy.deepcopy(chessboard)  # Copy Chessboard

                # Simulate the castling move
                sim_chessboard[7][6] = 'K' 
                sim_chessboard[7][5] = 'R'

                # Check if castling would leave the king in check
                if not is_check(sim_chessboard, is_white):
                    castling_moves.append((7,6))

    else:  # Black castling

            if "q" in possible_castling:  # Queenside castling
                logger.debug("q detected")

                # Check if squares between king and rook are empty
                Q_possible = chessboard[0][1] == 0 and chessboard[0][2] == 0 and chessboard[0][3] == 0  

                if Q_possible:
                    sim_chessboard = copy.deepcopy(chessboard)  # Copy Chessboard

                    # Simulate the castling move
                    sim_chessboard[0][2] = 'k' 
                    sim_chessboard[0][3] = 'r'

                    # Check if castling would leave the king in check
                    if not is_check(sim_chessboard, is_white):
                        castling_moves.append((0,2))

            if "k" in possible_castling:  # Kingside castling
                # Check if squares between king and rook are empty
                K_possible = chessboard[0][5] == 0 and chessboard[0][6] == 0 

                if K_possible:
                    sim_chessboard = copy.deepcopy(chessboard)  # Copy Chessboard

                    # Simulate the castling move
                    sim_chessboard[0][6] = 'k' 
                    sim_chessboard[0][5] = 'r'

                    # Check if castling would leave the king in check
                    if not is_check(sim_chessboard, is_white):
                        castling_moves.append((0,6))                

    return castling_moves


# Check if en passant is legal and return possible en passant moves
def legal_en_passant_moves(possible_en_passant, chessboard, is_white):

    en_passant_moves = {}

    # If no en passant target square is specified in the FEN string
    if possible_en_passant == '-':
        return {}

    # If an en passant target square is specified
    else:
        # Convert the en passant target square from algebraic notation (e.g., 'e6')
        # to a tuple of (row, column) where (0, 0) is the top-left square.
        en_passant_move = list(possible_en_passant)
        column = en_passant_move[0]
        converted_column = ord(column) - ord("a")  # e.g., 'a' -> 0, 'b' -> 1, ..., 'h' -> 7
        converted_row = 7 - (int(en_passant_move[1]) - 1) # e.g., '6' -> row 2 (0-indexed)

        converted_en_passant_move = (converted_row, converted_column)
        logger.debug(converted_en_passant_move)

        # If the en passant target row is the 5th rank (for black's pawn capture)
        if converted_row == 5:
            # Check for black pawns that can make the en passant capture
            logger.debug("CHECK FIELDS")
            for field in [-1, +1]: # Check the squares to the left and right of the target square
                # Check if the adjacent square contains a black pawn and is within the board boundaries
                if in_bound(converted_row - 1, converted_column + field) and chessboard[converted_row - 1][converted_column + field] == 'p':

                    # Simulate the en passant move
                    sim_chessboard = copy.deepcopy(chessboard)
                    sim_chessboard[converted_row][converted_column] = 'p' # Place the capturing pawn on the target square
                    sim_chessboard[converted_row - 1][converted_column + field] = 0 

                    sim_chessboard[converted_row - 1][converted_column] = 0 # remove captured white pawn

                    logger.debug(f"Checking p on{converted_row - 1}{converted_column + field} with Field = {field}")
                    logger.debug(sim_chessboard)
                    # Check if the move leaves the black king in check
                    if not is_check(sim_chessboard, is_white):
                        # If the move is legal, add it to the possible en passant moves
                        # The key is the starting position of the capturing pawn, the value is a list containing the target square
                        en_passant_moves.setdefault((converted_row - 1, converted_column + field), []).append(converted_en_passant_move)

            logger.debug("DONE")            

        # If the en passant target row is the 3rd rank (for white's pawn capture)
        elif converted_row == 3:
            # Check for white pawns that can make the en passant capture
            for field in [-1, +1]: # Check the squares to the left and right of the target square
                # Check if the adjacent square contains a white pawn and is within the board boundaries
                if in_bound(converted_row + 1, converted_column + field) and chessboard[converted_row + 1][converted_column + field] == 'P':

                    # Simulate the en passant move
                    sim_chessboard = copy.deepcopy(chessboard)
                    sim_chessboard[converted_row][converted_column] = 'P' # Place the capturing pawn on the target square
                    sim_chessboard[converted_row + 1][converted_column + field] = 0 


                    sim_chessboard[converted_row + 1][converted_column] = 0 # remove captured black pawn

                    # Check if the move leaves the white king in check
                    if not is_check(sim_chessboard, is_white):
                        # If the move is legal, add it to the possible en passant moves
                        # The key is the starting position of the capturing pawn, the value is a list containing the target square
                        en_passant_moves.setdefault((converted_row + 1, converted_column + field), []).append(converted_en_passant_move)

                       
    return en_passant_moves
    

# Simulate a move and return the resulting board state
def make_move(key, move, chessboard_object): 

    sim_chessboard = copy.deepcopy(chessboard_object.chessboard)  # Create a deep copy of the board

    piece = sim_chessboard[key[0]][key[1]]  # Get the piece to move

    sim_chessboard[key[0]][key[1]] = 0  # Remove piece from original position
    sim_chessboard[move[0]][move[1]] = piece  # Place piece at new position

    # Create a new chessboard state with the updated position
    new_chessboard_object = Chessboard_state(sim_chessboard, chessboard_object.castling, chessboard_object.en_passant)
    
    return new_chessboard_object


# Check if the king of the given color is in check
def is_check(chessboard, is_white):

    # Get all possible moves by the opponent
    all_opponent_moves = generate_moves(chessboard, not is_white)
    king_field = get_king_field(chessboard, is_white)  # Find the king's position

    # Check if any opponent move can capture the king
    for key, value in all_opponent_moves.items():
        
        if (len(value) != 0): 
           
            for move in value: 

                if move == king_field:  # King is attacked -> check
                    return True
                
    return False  # King is not attacked            
 

# Check if the game is over (checkmate or stalemate)
def game_over(chessboard_object, is_white):

    legal_moves = len(generate_legal_moves(chessboard_object, is_white)) 

    if legal_moves != 0:  # If there are legal moves, game continues
        return False, None
    
    elif is_check:  # No legal moves and king in check = checkmate
        return True, 0
    
    else:  # No legal moves and king not in check = stalemate
        return True, 1
    

# Find the position of the king for a given color
def get_king_field(chessboard, is_white):

    for i in range(8):
        for j in range(8):

            if is_white and chessboard[i][j] == 'K':  # White king
                return (i,j)

            elif not is_white and chessboard[i][j] == 'k':  # Black king
                return (i,j) 
            
    return (-1,-1)  # No king found (should never happen in a legal position)

    
# Generate all possible pawn moves
def pawn_moves(field_row, field_column, is_white, chessboard):
    possible_moves = []

    # Set direction and starting row based on color
    if is_white:
        forward_row = field_row - 1
        start_row = 6
        direction = -1  # White moves up
    else:
        forward_row = field_row + 1
        start_row = 1
        direction = 1  # Black moves down

    # One square forward if empty
    if chessboard[forward_row][field_column] == 0:
        possible_moves.append((forward_row, field_column))

        # Two squares forward from starting position if both squares are empty
        if field_row == start_row and chessboard[forward_row + direction][field_column] == 0:
            possible_moves.append((forward_row + direction, field_column))

    # Check diagonal captures
    for side in [-1, 1]:  # -1 = left, +1 = right
        new_column = field_column + side
        if 0 <= new_column <= 7:  # Check if within board boundaries
            target_piece = chessboard[forward_row][new_column]
            if target_piece != 0 and is_enemy(is_white, target_piece):  # Enemy piece there?
                possible_moves.append((forward_row, new_column))

    return possible_moves


# Generate all possible bishop moves
def bishop_moves(field_row, field_column, is_white, chessboard):

    move_pattern = constants.Piece_moves.Bishop  # Get bishop movement directions
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Starting position

        # Continue moving in the direction until blocked
        while in_bound(row + direction[0], column + direction[1]):

            row += direction[0]  # Vertical movement
            column += direction[1]  # Horizontal movement

            if chessboard[row][column] == 0:  # Empty square
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):  # Enemy piece
                possible_moves.append((row, column))
                break  # Enemy blocks further movement

            else:  # Own piece blocks movement
                break

    return possible_moves


# Generate all possible knight moves
def knight_moves(field_row, field_column, is_white, chessboard):
    
    move_pattern = constants.Piece_moves.Knight  # Get knight movement directions
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Starting position

        # Check if the target square is within the board
        if in_bound(row + direction[0], column + direction[1]):

            row += direction[0]  # Vertical movement
            column += direction[1]  # Horizontal movement

            if chessboard[row][column] == 0:  # Empty square
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):  # Enemy piece
                possible_moves.append((row, column))
                
            # Own piece blocks movement (no else needed)

    return possible_moves


# Generate all possible rook moves
def rook_moves(field_row, field_column, is_white, chessboard):

    move_pattern = constants.Piece_moves.Rook  # Get rook movement directions
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Starting position

        # Continue moving in the direction until blocked
        while in_bound(row + direction[0], column + direction[1]):

            row += direction[0]  # Vertical movement
            column += direction[1]  # Horizontal movement

            if chessboard[row][column] == 0:  # Empty square
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):  # Enemy piece
                possible_moves.append((row, column))
                break  # Enemy blocks further movement

            else:  # Own piece blocks movement
                break

    return possible_moves


# Generate all possible queen moves
def queen_moves(field_row, field_column, is_white, chessboard):
    
    move_pattern = constants.Piece_moves.Queen  # Get queen movement directions (combination of rook and bishop)
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Starting position

        # Continue moving in the direction until blocked
        while in_bound(row + direction[0], column + direction[1]):

            row += direction[0]  # Vertical movement
            column += direction[1]  # Horizontal movement

            if chessboard[row][column] == 0:  # Empty square
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):  # Enemy piece
                possible_moves.append((row, column))
                break  # Enemy blocks further movement

            else:  # Own piece blocks movement
                break

    return possible_moves
        

# Generate all possible king moves
def king_moves(field_row, field_column, is_white, chessboard):
    
    move_pattern = constants.Piece_moves.King  # Get king movement directions
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Starting position

        # Check if the target square is within the board
        if in_bound(row + direction[0], column + direction[1]):

            row += direction[0]  # Vertical movement
            column += direction[1]  # Horizontal movement

            if chessboard[row][column] == 0:  # Empty square
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):  # Enemy piece
                possible_moves.append((row, column))

    return possible_moves
        

# Check if a position is within the board boundaries
def in_bound(row, column):
    return 0 <= row <= 7 and 0 <= column <= 7 


# Check if a piece is an enemy piece based on color
def is_enemy(is_white, figure):
    return str.islower(figure) if is_white else str.isupper(figure)


# Class to represent the state of a chessboard
class Chessboard_state:

    def __init__(self, chessboard, castling, en_passant):
        self.chessboard = chessboard  # 2D array representing the board
        self.castling = castling  # Castling rights
        self.en_passant = en_passant  # En passant target square


# Run the Flask app if this file is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)