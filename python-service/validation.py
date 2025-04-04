from flask import Flask, request
import urllib.parse
import logging
import constants
import searchfunction
import copy


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()

app = Flask(__name__)

Pieces = constants.Pieces

# Retuns best move found by searchfunction {from: ... , to: ...} TODO Promotion
@app.route('/best-move', methods=['POST'])
def get_best_move():
        
    data = request.get_json()

    is_white = data["is_white"]

    received_fen = data["fen"]  # String has to be decoded -> String recieved as Bytes
    formatted_fen = urllib.parse.unquote(received_fen) # Return to ASCII-notation of FEN


    chessboard_object = fen_to_chessboard_object(formatted_fen)
    
    logger.debug(chessboard_object.chessboard)

    searchfunction.counter = 0 # Reset Counter

    best_move = searchfunction.MINIMAX(chessboard_object, 2, is_white, searchfunction.Move(0,0))
    logger.debug(best_move.to_dict)

    fen_to_chessboard_object(formatted_fen)

    return best_move.to_dict() # Return best move


# Evaluates current chessboard
def evaluate_position(chessboard):

    value = 0
    value += calc_piece_value_with_psqt(chessboard)

    return value



def fen_to_chessboard_object(fen):
    

    chessboard_fen, information_fen = fen.split(" ",1) 
    chessboard = fen_to_array(chessboard_fen)

    turn_right, rochade, en_passant, halfmove, fullmove = information_fen.split(" ")

    chessboard_object = Chessboard_state(chessboard, rochade, en_passant)

    logger.debug(chessboard)
    # logger.debug(f"Turn: {chessboard_object.turn_right}, Rochade: {chessboard_object.rochade}, En Passant: {chessboard_object.en_passant}, Halfmove: {chessboard_object.halfmove}, Fullmove: {chessboard_object.fullmove}")


    return chessboard_object



# Convert FEN into 2D Array
def fen_to_array(fen):
    
    # 2D Array 8x8
    chessboard = [[0 for _ in range(8)] for _ in range(8)]

    current_field = 0
    current_row = 0
    current_column = 0


    for char in fen: 

        if char.isalpha():
            current_row = current_field // 8
            current_column = current_field % 8
            chessboard[current_row][current_column] = char
            current_field += 1
           

        elif char.isdigit():
            current_field += int(char)

        elif char == " ":
            break

    return chessboard



# Return piece-value-difference based of piece-value and PSQT 
def calc_piece_value_with_psqt(chessboard): # TODO incremental 

    value = 0
    currentField = 0

    # Iterate trought 2D Array
    for i in range(8): 
        for j in range(8): 

            char = chessboard[i][j]

            if char == 0:
                currentField += 1


            elif char.isupper(): # White
                psqtValue = get_psqt_value(currentField, char, True)
                value += getattr(Pieces, char, 0) + psqtValue

                currentField += 1 


            elif char.islower(): # Black
                psqtValue = get_psqt_value(currentField, char, False)
                value -= getattr(Pieces, char.upper(), 0) + psqtValue
            
                currentField += 1

   
    return value



# Return PSQT Value of given piece on given field
def get_psqt_value(field, piece, is_white):

    psqt = get_psqt_table(piece, is_white)
    kingOrQueen = piece.upper() == "K" or piece.upper() == "Q"

        
    if not is_white or kingOrQueen:  # Check if king or queen is currently evaluated to correctly access mirrored PSQT
        return psqt[63 - field]  # Return mirrored value
    else:
         return psqt[field] # Else return 
        
        

# Return PSQT Table of piece
def get_psqt_table(piece, is_white):
    
    match piece.upper():
        case 'P': return constants.Psqt.PAWN_PSQT
        case 'R': return constants.Psqt.ROOK_PSQT
        case 'B': return constants.Psqt.BISHOP_PSQT
        case 'N': return constants.Psqt.KNIGHT_PSQT
        case 'Q': return get_queen_psqt(is_white)
        case 'K': return get_king_psqt(is_white)
        case _: logger.error(f"no PSQT found for {piece}"); return -1  



# Return white or black King-PSQT
def get_king_psqt(is_white):
    if is_white:
        return constants.Psqt.KING_PSQT
    else:
        return constants.Psqt.KING_PSQT_BLACK



# Return white or black Queen-PSQT
def get_queen_psqt(is_white):
    if is_white:
        return constants.Psqt.QUEEN_PSQT
    else:
        return constants.Psqt.QUEEN_PSQT_BLACK



# Returns 2D array of all possible moves for black or white for given position
# TODO Add Turn_object for en passent etc.
def generate_moves(chessboard, is_white):
    
    moves = {} # Dic for all moves

    for i in range(8):
        for j in range(8):

            piece = chessboard[i][j]

            if piece == 0:
                continue
                

            if piece.isupper() and is_white:

                match piece:
                    case 'P': moves.setdefault((i, j),[]).extend(pawn_moves(i, j, True, chessboard))
                    case 'B': moves.setdefault((i, j),[]).extend(bishop_moves(i, j, True, chessboard))
                    case 'N': moves.setdefault((i, j),[]).extend(knight_moves(i, j, True, chessboard))
                    case 'R': moves.setdefault((i, j),[]).extend(rook_moves(i,  j, True, chessboard))
                    case 'Q': moves.setdefault((i, j),[]).extend(queen_moves(i, j, True, chessboard))
                    case 'K': moves.setdefault((i, j),[]).extend(king_moves(i, j, True, chessboard))

            elif piece.islower() and not is_white: 

                match piece:
                    case 'p': moves.setdefault((i, j),[]).extend(pawn_moves(i, j, False, chessboard))
                    case 'b': moves.setdefault((i, j),[]).extend(bishop_moves(i, j, False, chessboard))
                    case 'n': moves.setdefault((i, j),[]).extend(knight_moves(i, j, False, chessboard))
                    case 'r': moves.setdefault((i, j),[]).extend(rook_moves(i, j, False, chessboard))
                    case 'q': moves.setdefault((i, j),[]).extend(queen_moves(i, j, False, chessboard))
                    case 'k': moves.setdefault((i, j),[]).extend(king_moves(i, j, False, chessboard))

    return moves
     

# Retuns all legal moves for black or white for given chessboard
def generate_legal_moves(chessboard_object, is_white):


    chessboard = chessboard_object.chessboard

    # rochade = rochade_moves(chessboard_object.rochade, chessboard_object.chessboard, is_white)
    # en_passant = en_passant_moves(chessboard_object.en_passant, is_white)

    all_moves = generate_moves(chessboard, is_white) # Generate all possible moves for black or white (is_white)
    legal_moves = {}
    
    for key, value in all_moves.items():
        
        if (len(value) != 0): 
           
            for move in value:

                sim_chessboard = make_move(key, move, chessboard_object).chessboard # Simulate move

                if not is_check(sim_chessboard, is_white): 
                    legal_moves.setdefault(key,[]).append((move[0], move[1])) # Add legal move
                

    return legal_moves




def rochade_moves(possible_rochade, chessboard, is_white):
    
    if possible_rochade == "-":
        return None

    if is_white:
        Q_possible = chessboard[7][1] == 0 and chessboard[7][2] == 0 and chessboard[7][3] == 0 
        K_possible = chessboard[7][5] == 0 and chessboard[7][6] == 0


    return 



    
    


# Simulates move from key to move on chessboard, returns new chessboard
def make_move(key, move, chessboard_object): 

    sim_chessboard = copy.deepcopy(chessboard_object.chessboard) # Copy Chessboard

    piece = sim_chessboard[key[0]][key[1]] # Get current piece

    sim_chessboard[key[0]][key[1]] = 0 # Remove Figure
    sim_chessboard[move[0]][move[1]] = piece


    new_chessboard_object = Chessboard_state(sim_chessboard, chessboard_object.rochade, chessboard_object.en_passant)
    
    return new_chessboard_object


# Returns true if current chessboard results in check, else false
def is_check(chessboard, is_white):

    all_opponent_moves = generate_moves(chessboard, not is_white) # Returns all possible moves of opponent
    king_field = get_king_field(chessboard, is_white)

    for key, value in all_opponent_moves.items(): # Iterate trough all opponents moves
        
        if (len(value) != 0): 
           
            for move in value: 

                if move == king_field: # King is attacked -> check
                    return True
                
    
    return False # King is not attacked            
 


# Returns tupel (is_gamemover, reason) 
# true, 0 if matt
# true, 1 if patt
# false, none if still legal moves left
def game_over(chessboard_object, is_white):

    legal_moves = len(generate_legal_moves(chessboard_object, is_white)) 

    if legal_moves != 0:
        return False, None
    
    elif is_check:
        return True, 0
    
    else:
        return True, 1
    


    

# Returns field king is on for black or white 
def get_king_field(chessboard, is_white):

    for i in range(8):
        for j in range(8):

            if is_white and chessboard[i][j] == 'K':
                return (i,j)

            elif not is_white and chessboard[i][j] == 'k':
                return (i,j) 
            
        
    return (-1,-1) # No King found

    
    
# TODO en passent etc.
# Returns all possible pawn moves on field (field_row, field_column) for black or white
def pawn_moves(field_row, field_column, is_white, chessboard):
    possible_moves = []


    if is_white:
        forward_row = field_row - 1
        start_row = 6
        direction = -1  # Weiß zieht nach oben
    else:
        forward_row = field_row + 1
        start_row = 1
        direction = 1  # Schwarz zieht nach unten

    # Ein Feld vorwärts, wenn frei
    if chessboard[forward_row][field_column] == 0:
        possible_moves.append((forward_row, field_column))

        # Zwei Felder vorwärts, wenn Startposition und beide Felder frei
        if field_row == start_row and chessboard[forward_row + direction][field_column] == 0:
            possible_moves.append((forward_row + direction, field_column))

    # Schlagzüge nach links und rechts prüfen
    for side in [-1, 1]:  # -1 = links, +1 = rechts
        new_column = field_column + side
        if 0 <= new_column <= 7:  # Prüfen, ob innerhalb der Spielfeldgrenzen
            target_piece = chessboard[forward_row][new_column]
            if target_piece != 0 and is_enemy(is_white, target_piece):  # Feindliche Figur dort?
                possible_moves.append((forward_row, new_column))

    
    return possible_moves


# Returns all possible bishop moves on field (field_row, field_column) for black or white
def bishop_moves(field_row, field_column, is_white, chessboard):

    move_pattern = constants.Piece_moves.Bishop
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Startposition

        while in_bound(row + direction[0], column + direction[1]):

            row += direction[0] # directioion[0] stores vertical movement
            column += direction[1] # directioion[0] stores horizontal movement

            if chessboard[row][column] == 0:
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):
                possible_moves.append((row, column))
                break  # Gegner blockiert weitere Bewegung

            else: # Eigene Figur blockiert Bewegung
                break

    return possible_moves


# Returns all possible knight moves on field (field_row, field_column) for black or white
def knight_moves(field_row, field_column, is_white, chessboard):
    
    move_pattern = constants.Piece_moves.Knight
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Startposition

        if in_bound(row + direction[0], column + direction[1]):

            row += direction[0] # directioion[0] stores vertical movement
            column += direction[1] # directioion[0] stores horizontal movement

            if chessboard[row][column] == 0:
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):  #Gegner blockiert weitere Bewegung
                possible_moves.append((row, column))
                
            #else: # Eigene Figur blockiert Bewegung
            #   logger.debug(f"Knight blocked by own piece {row}, {column}")

    return possible_moves


# Returns all possible rook moves field (field_row, field_column) for black or white
def rook_moves(field_row, field_column, is_white, chessboard):

    move_pattern = constants.Piece_moves.Rook
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Startposition

        while in_bound(row + direction[0], column + direction[1]):

            row += direction[0] # directioion[0] stores vertical movement
            column += direction[1] # directioion[0] stores horizontal movement

            if chessboard[row][column] == 0:
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):
                possible_moves.append((row, column))
                break  # Gegner blockiert weitere Bewegung

            else: # Eigene Figur blockiert Bewegung
                break

    return possible_moves


# Returns all possible queen moves on field (field_row, field_column) for black or white
def queen_moves(field_row, field_column, is_white, chessboard):
    
    move_pattern = constants.Piece_moves.Queen
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Startposition

        while in_bound(row + direction[0], column + direction[1]):

            row += direction[0] # directioion[0] stores vertical movement
            column += direction[1] # directioion[0] stores horizontal movement

            if chessboard[row][column] == 0:
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):
                possible_moves.append((row, column))
                break  # Gegner blockiert weitere Bewegung

            else: # Eigene Figur blockiert Bewegung
                break

    return possible_moves
        

# Returns all possible king moves on field (field_row, field_column) for black or white
def king_moves(field_row, field_column, is_white, chessboard):
    
    move_pattern = constants.Piece_moves.King
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Startposition

        if in_bound(row + direction[0], column + direction[1]):

            row += direction[0] # directioion[0] stores vertical movement
            column += direction[1] # directioion[0] stores horizontal movement

            if chessboard[row][column] == 0:
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]): # Gegner blockiert weitere Bewegung
                possible_moves.append((row, column))


    return possible_moves
        


# Checks if (row, column) is still on chessboard
def in_bound(row, column):
    return 0 <= row <= 7 and 0 <= column <= 7 


# Returns true if figure is an enemy piece, else false
def is_enemy(is_white, figure):
    return str.islower(figure) if is_white else str.isupper(figure)





class Chessboard_state:

    def __init__(self, chessboard, rochade, en_passant):
        self.chessboard = chessboard
        self.rochade = rochade
        self.en_passant = en_passant



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
