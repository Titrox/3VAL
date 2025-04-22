from flask import Flask, request
import urllib.parse
import logging
import constants
import searchfunction
import copy
from flask import jsonify


# Setting up basic logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()

# Initialize Flask application
app = Flask(__name__)

Pieces = constants.Pieces
standard_pieces = constants.Standard_pieces


###
#
# API
#
###

# Flask route to get the best move using the minimax algorithm
# Returns a dictionary with 'from' and 'to' fields
@app.route('/best-move', methods=['POST'])
def get_best_move_api():  # pragma: no cover

    # Define infinity values for minimax algorithm
    INFINITY = float('inf')
    NEG_INFINITY = float('-inf')
        
    data = request.get_json()

    is_white = data["is_white"]  # Boolean indicating if it's white's turn

    received_fen = data["fen"]  # Get the FEN string from the request

    formatted_fen = urllib.parse.unquote(received_fen)  # Decode URL-encoded FEN string to ASCII


    chessboard_object = fen_to_chessboard_object(formatted_fen)  # Convert FEN to chessboard object

    searchfunction.counter = 0  # Reset search counter

    # Search for the best move with depth 3
    best_move = searchfunction.MINIMAX(chessboard_object, 0, 3, is_white, searchfunction.Move(0,0), NEG_INFINITY, INFINITY)
    logger.debug(f"{best_move.start, best_move.end}")
   

    fen_to_chessboard_object(formatted_fen)

    return best_move.to_dict()  # Return the best move found





@app.route('/evaluate-position', methods=['POST'])
def evaluate_position_api():  # pragma: no cover

    data = request.get_json()
    logger.debug(data)
    fen = data["fen"]

    chessboard = fen_to_array(fen)
    
    
    return str(evaluate_position(chessboard))



@app.route('/get-evaluation-factors', methods=['GET'])
def get_evaluation_factors():  # pragma: no cover

    evaluation_factors = {
    
    # evaluation factors
    "centerControlValue": constants.Standard_evaluation_factors.DYNAMIC_CONTROL,
    "knightOutpostValue": constants.Standard_evaluation_factors.KNIGHT_OUTPOST,
    "badBishopValue": constants.Standard_evaluation_factors.BAD_BISHOP,
    "pawnShieldValue": constants.Standard_evaluation_factors.KING_SAFETY_PAWN_SHIELD,
    "virtualMobilityValue": constants.Standard_evaluation_factors.KING_SAFETY_VIRTUAL_MOBILITY,
    "queenEarlyDevValue": constants.Standard_evaluation_factors.QUEEN_EARLY_DEVELOPMENT_PENALTY,

    # piece values
    "queenValue": constants.Standard_pieces.Q,
    "rookValue": constants.Standard_pieces.R,
    "bishopValue": constants.Standard_pieces.B,
    "knightValue": constants.Standard_pieces.N,
    "pawnValue": constants.Standard_pieces.P
}

    resetEvaluationFactors() 
    
    return jsonify(evaluation_factors)
    
    

@app.route('/put-evaluation-factors', methods=['PUT'])
def put_evaluation_factors():  # pragma: no cover

    data = request.get_json()


    # Update factors  
    constants.Evaluation_factors.DYNAMIC_CONTROL = float(data["centerControlValue"])
    constants.Evaluation_factors.KNIGHT_OUTPOST = float(data["knightOutpostValue"])
    constants.Evaluation_factors.BAD_BISHOP = float(data["badBishopValue"])
    constants.Evaluation_factors.KING_SAFETY_PAWN_SHIELD = float(data["pawnShieldValue"])
    constants.Evaluation_factors.KING_SAFETY_VIRTUAL_MOBILITY = float(data["virtualMobilityValue"]) 
    constants.Evaluation_factors.QUEEN_EARLY_DEVELOPMENT_PENALTY = float(data["queenEarlyDevValue"])

    # Update piece values
    constants.Pieces.Q = float(data["queenValue"])
    constants.Pieces.R = float(data["rookValue"])
    constants.Pieces.B = float(data["bishopValue"])
    constants.Pieces.N = float(data["knightValue"])
    constants.Pieces.P = float(data["pawnValue"])


    return jsonify({"status": "success", "message": "Evaluation factors updated successfully"}), 200



@app.route('/reset-evaluation-factors', methods=['POST'])
def rest_evaluation_factors():  # pragma: no cover

    resetEvaluationFactors()

    return jsonify({"status": "success", "message": "Evaluation factors reseted successfully"}), 200




# Resets factors used by evaluation function to standard values
def resetEvaluationFactors():

    # Reset evaluation factors
    constants.Evaluation_factors.DYNAMIC_CONTOL = constants.Standard_evaluation_factors.DYNAMIC_CONTROL
    constants.Evaluation_factors.KNIGHT_OUTPOST = constants.Standard_evaluation_factors.KNIGHT_OUTPOST
    constants.Evaluation_factors.BAD_BISHOP = constants.Standard_evaluation_factors.BAD_BISHOP
    constants.Evaluation_factors.KING_SAFETY_PAWN_SHIELD = constants.Standard_evaluation_factors.KING_SAFETY_PAWN_SHIELD
    constants.Evaluation_factors.KING_SAFETY_VIRTUAL_MOBILITY = constants.Standard_evaluation_factors.KING_SAFETY_VIRTUAL_MOBILITY
    constants.Evaluation_factors.QUEEN_EARLY_DEVELOPMENT_PENALTY = constants.Standard_evaluation_factors.QUEEN_EARLY_DEVELOPMENT_PENALTY


    # Reset piece values
    constants.Pieces.Q = standard_pieces.Q
    constants.Pieces.R = standard_pieces.R
    constants.Pieces.B = standard_pieces.B
    constants.Pieces.N = standard_pieces.N
    constants.Pieces.P = standard_pieces.P


###
#
# HANDLE FEN
#
###    


# Convert FEN string to a chessboard object
def fen_to_chessboard_object(fen):  # pragma: no cover
    
    # Split FEN into board position and game information
    chessboard_fen, information_fen = fen.split(" ",1) 
    chessboard = fen_to_array(chessboard_fen)  # Convert the position part to a 2D array

    # Extract additional information from FEN
    turn_right, castling, en_passant, halfmove, fullmove = information_fen.split(" ")

    # Create a chessboard state object with the position and castling/en passant rights
    chessboard_object = Chessboard_state(chessboard, castling, en_passant, None)

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



###
#
# PSQT
#
###    



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
                
            else:

                is_white = char.isupper()

                psqtValue = get_psqt_value(currentField, char, is_white)  # Get position value
                
                match char.upper():
                    case 'P': pieceValue = Pieces.P
                    case 'R': pieceValue = Pieces.R
                    case 'B': pieceValue = Pieces.B
                    case 'N': pieceValue = Pieces.N
                    case 'Q': pieceValue = Pieces.Q
                    case _: pieceValue = 0  

                currentField += 1 
                
                if is_white:
                    value += psqtValue + pieceValue # Add piece value and position value 
                else:
                    value -= psqtValue + pieceValue # Add piece value and position value

   
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
    

###
#
# MOVE GENERATION
#
###    



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
    
    # logger.debug(f"En Passant: {en_passant_moves}")

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

    # logger.debug(legal_moves)

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

        # If the en passant target row is the 5th rank (for black's pawn capture)
        if converted_row == 5:
            # Check for black pawns that can make the en passant capture
            for field in [-1, +1]: # Check the squares to the left and right of the target square
                # Check if the adjacent square contains a black pawn and is within the board boundaries
                if in_bound(converted_row - 1, converted_column + field) and chessboard[converted_row - 1][converted_column + field] == 'p':

                    # Simulate the en passant move
                    sim_chessboard = copy.deepcopy(chessboard)
                    sim_chessboard[converted_row][converted_column] = 'p' # Place the capturing pawn on the target square
                    sim_chessboard[converted_row - 1][converted_column + field] = 0 

                    sim_chessboard[converted_row - 1][converted_column] = 0 # remove captured white pawn

                    # Check if the move leaves the black king in check
                    if not is_check(sim_chessboard, is_white):
                        # If the move is legal, add it to the possible en passant moves
                        # The key is the starting position of the capturing pawn, the value is a list containing the target square
                        en_passant_moves.setdefault((converted_row - 1, converted_column + field), []).append(converted_en_passant_move)    

        # If the en passant target row is the 3rd rank (for white's pawn capture)
        elif converted_row == 2:
            logger.debug("TEST")
            # Check for white pawns that can make the en passant capture
            for field in [-1, +1]: # Check the squares to the left and right of the target square
                # Check if the adjacent square contains a white pawn and is within the board boundaries
                logger.debug(f" In bound: {in_bound(converted_row + 1, converted_column + field)}")
                logger.debug(f"Check Pawn on: {converted_row + 1}, {converted_column + field}")
                logger.debug(f"Pawn found? {chessboard[converted_row + 1][converted_column + field] == 'P'}")
                

                if in_bound(converted_row + 1, converted_column + field) and chessboard[converted_row + 1][converted_column + field] == 'P':

                    # Simulate the en passant move
                    sim_chessboard = copy.deepcopy(chessboard)
                    sim_chessboard[converted_row][converted_column] = 'P' # Place the capturing pawn on the target square
                    sim_chessboard[converted_row + 1][converted_column + field] = 0 

                    logger.debug("SIm move")


                    sim_chessboard[converted_row + 1][converted_column] = 0 # remove captured black pawn

                    # Check if the move leaves the white king in check
                    if not is_check(sim_chessboard, is_white):
                        # If the move is legal, add it to the possible en passant moves
                        # The key is the starting position of the capturing pawn, the value is a list containing the target square
                        en_passant_moves.setdefault((converted_row + 1, converted_column + field), []).append(converted_en_passant_move)

                       
    return en_passant_moves
    

# Simulate a move and return the resulting board state
def make_move(start, end, chessboard_object): 

    sim_chessboard = copy.deepcopy(chessboard_object.chessboard)  # Create a deep copy of the board
    piece = sim_chessboard[start[0]][start[1]]  # Get the piece to move

    is_white = piece.isupper()

    # PROMOTION

    if ((end[0] == 0 or end[0] == 7) and piece.lower() == 'p'): # Pawn has to promote


        #logger.debug(f"Simulating: {move[0], move[1]}")
        #logger.debug("Pawn on last lane")

        if is_white:
            piece = 'Q'
        else: 
            piece = 'q'


    sim_chessboard[start[0]][start[1]] = 0  # Remove piece from original position
    sim_chessboard[end[0]][end[1]] = piece  # Place piece at new position


    # Create a new chessboard state with the updated position
    new_chessboard_object = Chessboard_state(sim_chessboard, chessboard_object.castling, chessboard_object.en_passant, piece)
    
    return new_chessboard_object

    
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


   

    if in_bound(forward_row, field_column):

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

    move_pattern = constants.Piece_moves.BISHOP  # Get bishop movement directions
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
    
    move_pattern = constants.Piece_moves.KNIGHT  # Get knight movement directions
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

    move_pattern = constants.Piece_moves.ROOK  # Get rook movement directions
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
    
    move_pattern = constants.Piece_moves.QUEEN  # Get queen movement directions (combination of rook and bishop)
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
    
    move_pattern = constants.Piece_moves.KING  # Get king movement directions
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



###
#
# HELPER FUNCTIONS
#
###    


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
    chessboard = chessboard_object.chessboard

    if legal_moves != 0:  # If there are legal moves, game continues
        return False, None
    
    elif is_check(chessboard, is_white):  # No legal moves and king in check = checkmate
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

        

# Check if a position is within the board boundaries
def in_bound(row, column):
    return 0 <= row <= 7 and 0 <= column <= 7 


# Check if a piece is an enemy piece based on color
def is_enemy(is_white, figure):
    return str.islower(figure) if is_white else str.isupper(figure)



###
#
# EVALUATION FUNCTION
#
###

    # Evaluates current chessboard position
def evaluate_position(chessboard):  # pragma: no cover

    value = 0
    value += calc_piece_value_with_psqt(chessboard)  # Calculate value based on pieces and their positions TODO integrate in for loop

    black_king_position = get_king_field(chessboard, False)
    white_king_position = get_king_field(chessboard, True)


    pawn_counter = 0 # Keep track of pawns on field for estimation of game progress
    white_rooks = 0  
    black_rooks = 0

    for i in range(8):
        for j in range (8):

            piece = chessboard[i][j]

            if piece != 0: # Only evaluate relevant fields (no empty fields)


                # Keep track of pawns on field for estimation of game progress
                
                if piece.lower() == 'p':
                    pawn_counter += 1

                    # King Tropism

                    distance = distance_to_king(i, j, white_king_position) if piece.islower() else distance_to_king(i, j, black_king_position)  
                    value += king_tropism(distance, piece)


                # Keep track of rooks on field  

                if piece.lower() == 'r':

                    if piece.isupper():
                        white_rooks += 1
                    else:
                        black_rooks +=1

                    # King Tropism

                    distance = distance_to_king(i, j, white_king_position) if piece.islower() else distance_to_king(i, j, black_king_position)  
                    value += king_tropism(distance, piece)




                # Center fields - Dynamic Control

                if 2 < i < 5 and 2 < j < 5: 
                    value += constants.Evaluation_factors.DYNAMIC_CONTROL * dynamic_control(piece, chessboard, i, j)


                # King Safety

                if piece.lower() == 'k': # King detected
                    value += king_safety(chessboard, piece.isupper(), i, j)


                # EVALUATION OF PIECES


                # Outpost - Knight defended by pawn

                if piece.lower() == 'n': # Knight detected
                    value += constants.Evaluation_factors.KNIGHT_OUTPOST * knight_outpost(chessboard, piece.isupper(), i, j)

                    distance = distance_to_king(i, j, white_king_position) if piece.islower() else distance_to_king(i, j, black_king_position)  
                    value += king_tropism(distance, piece)

                # Bad Bishop - Bishop blocked by own pawns

                if piece.lower() == 'b': # Bishop detected
                    value += constants.Evaluation_factors.BAD_BISHOP * bad_bishop(chessboard, piece.isupper(), i, j)

                    distance = distance_to_king(i, j, white_king_position) if piece.islower() else distance_to_king(i, j, black_king_position) 
                    value += king_tropism(distance, piece)

                # Queen early development penalty

                if piece.lower() == 'q': # Queen detected
                    value += early_queen_development_penalty(chessboard, piece.isupper(), pawn_counter)

                    distance = distance_to_king(i, j, white_king_position) if piece.islower() else distance_to_king(i, j, black_king_position) 
                    value += king_tropism(distance, piece)
                    #logger.debug(f"{piece} Tropism value: {king_tropism(distance, piece)}")



    # Increase rook value depending on pawns on field

    value += white_rooks * (14 - pawn_counter) ;
    value -= black_rooks * (14 - pawn_counter)


    return value


# KING SAFETY

def king_safety(chessboard, is_white, row, column):

    king_safety_value = 0
    
    king_safety_value += constants.Evaluation_factors.KING_SAFETY_PAWN_SHIELD * pawn_shield(chessboard, is_white, row, column)
    king_safety_value += constants.Evaluation_factors.KING_SAFETY_VIRTUAL_MOBILITY * virtual_mobility(chessboard, is_white, row, column)

    return king_safety_value


def distance_to_king(row, column, king_position):

    figure_x = column
    figure_y = row

    king_x = king_position[1]
    king_y = king_position[0]

    return  (abs(king_x - figure_x) + abs(king_y - figure_y))


def virtual_mobility(chessboard, is_white, row, column):

    possible_queen_moves = []
    possible_queen_moves = queen_moves(row, column, is_white, chessboard)
    

    return -len(possible_queen_moves) if is_white else len(possible_queen_moves)

        
def pawn_shield(chessboard, is_white, row, column):

    pawn_shield_value = 0

    if is_white:
        king_front_row = row -1
        pawn = 'P'
    else:
        king_front_row = row + 1
        pawn = 'p'


    for pawn_position in [1,0,-1]: # Check relevant fields vor pawns

        if in_bound(king_front_row, column + pawn_position):

            if chessboard[king_front_row][column + pawn_position] == pawn:
                pawn_shield_value += 1      


    return pawn_shield_value if is_white else -pawn_shield_value



def king_tropism(distance, piece):

    piece_type = piece.lower()
    is_white = piece.isupper()

    factors = {
        'q': 100,  # Queen: Sehr hoher Einfluss
        'r': 80,   # Rook: Hoher Einfluss
        'b': 60,   # Bishop: Mittlerer Einfluss
        'n': 50,   # Knight: Mittlerer Einfluss, kann in kurzer Distanz sehr wirksam sein
        'p': 20    # Pawn: Geringer Einfluss, kann in direkter Nähe gefährlich werden
    }

    value = round(factors.get(piece_type) / distance)
    return value if is_white else -value


# DYNAMIC CONTROL



def dynamic_control(piece, chessboard, row, column):

    is_white_figure = piece.isupper()
    possible_moves = [] # All possible moves for figure on field (row, column)


   
    if is_white_figure: 

        match piece:
            case 'P': possible_moves.extend(pawn_moves(row, column, True, chessboard))
            case 'B': possible_moves.extend(bishop_moves(row, column, True, chessboard))
            case 'N': possible_moves.extend(knight_moves(row, column, True, chessboard))
            case 'R': possible_moves.extend(rook_moves(row, column, True, chessboard))
            case 'Q': possible_moves.extend(queen_moves(row, column, True, chessboard))
            case 'K': possible_moves.extend(king_moves(row, column, True, chessboard))

    else: 

        match piece:
            case 'p': possible_moves.extend(pawn_moves(row, column, False, chessboard))
            case 'b': possible_moves.extend(bishop_moves(row, column, False, chessboard))
            case 'n': possible_moves.extend(knight_moves(row, column, False, chessboard))
            case 'r': possible_moves.extend(rook_moves(row, column, False, chessboard))
            case 'q': possible_moves.extend(queen_moves(row, column, False, chessboard))
            case 'k': possible_moves.extend(king_moves(row, column, False, chessboard))
            
    
    
    return len(possible_moves) if is_white_figure else -len(possible_moves)



# EVALUATION OF PIECES



# Returns 1 or -1 if knight is defended by pawn depending on color, else 0
def knight_outpost(chessboard, is_white, row, column):

    if is_white:
        behind_row = row + 1
        pawn = 'P'
    else:
        behind_row = row - 1
        pawn = 'p'


    for pawn_position in [1, -1]:

        if in_bound(behind_row, column + pawn_position) and chessboard[behind_row][column + pawn_position] == pawn:
            return 1 if is_white else -1 
    
    return 0


# Returns number of pawns blocking bishop
def bad_bishop(chessboard, is_white, row, column):

    blocking_pawns = 0

    if is_white:
        front_row = row - 1
        pawn = 'P'
    else:
        front_row = row + 1
        pawn = 'p'


    for pawn_position in [1, -1]:

        if in_bound(front_row, column + pawn_position) and chessboard[front_row][column + pawn_position] == pawn:
            
            blocking_pawns += 1



    return -blocking_pawns if is_white else blocking_pawns
    

# Returns penalty for early queen development depending on number of pawns 
def early_queen_development_penalty(chessboard, is_white, pawn_counter):

    penalty = constants.Evaluation_factors.QUEEN_EARLY_DEVELOPMENT_PENALTY 

    if is_white:
        queen_row = 7
        queen = 'Q'
    else:
        queen_row = 0
        queen = 'q'


    if pawn_counter >= 14 and chessboard[queen_row][3] != queen: # Opening game - full penalty
        logger.debug("You")
        return -penalty if is_white else penalty
        
        
    elif pawn_counter >= 10 and chessboard[queen_row][3] != queen: # Half pentalty
        return -(penalty / 2) if is_white else (penalty / 2)

        # Else no penalty

    else:
        return 0

# Class to represent the state of a chessboard
class Chessboard_state:

    def __init__(self, chessboard, castling, en_passant, promotion):
        self.chessboard = chessboard  # 2D array representing the board
        self.castling = castling  # Castling rights
        self.en_passant = en_passant  # En passant target square
        self.promotion = promotion


# Run the Flask app if this file is executed directly
if __name__ == "__main__":  # pragma: no cover
    app.run(host="0.0.0.0", port=5000, debug=True)