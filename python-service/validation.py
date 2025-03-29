from flask import Flask, request
import urllib.parse
import logging
import constants


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()

app = Flask(__name__)

Pieces = constants.Pieces


@app.route('/best-move', methods=['POST'])
def getBestMove():
        
    data = request.get_json()

    is_white = data["is_white"]

    received_fen = data["fen"]  # String has to be decoded -> String recieved as Bytes
    formatted_fen = urllib.parse.unquote(received_fen) # Return to ASCII-notation of FEN

    value = calcPieceValueWithPSQT(formatted_fen) # Calc current piece value of AIs pieces
    logger.debug(generate_moves(formatted_fen))
    return value  


# Convert FEN into 1D array for calculations
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

    logger.debug(chessboard)
    return chessboard


# Return Piece-Value-Difference based of piece-value and PSQT 
def calcPieceValueWithPSQT(fen): # TODO incremental 

    value = 0
    # logger.debug(fen)
    currentField = 0

    for char in fen: 
        if char.isupper(): # White
            psqtValue = getPsqtValue(currentField, char, True)
            value += getattr(Pieces, char, 0) + psqtValue

            # logger.debug(f"{char} : {getattr(Pieces, char, 0)} PSQRT: {psqtValue} Feld: {currentField} Value insgesamt: {getattr(Pieces, char, 0) + psqtValue}")
    
            currentField += 1 

        elif char.islower(): # Black
            psqtValue = getPsqtValue(currentField, char, False)
            value -= getattr(Pieces, char.upper(), 0) + psqtValue
            
            # logger.debug(f"{char} : {getattr(Pieces, char.upper(), 0)} PSQRT: {psqtValue} Feld: {currentField} Value insgesamt: {getattr(Pieces, char.upper(), 0) + psqtValue}")
            
            currentField += 1
        elif char.isdigit():
            currentField += int(char)
        if char == ' ':
            break
            
        # logger.debug(value)
    return str(value)



# Return PSQT Value of given piece on given field
def getPsqtValue(field, piece, is_white):

    psqt = getPsqtTable(piece, is_white)
    kingOrQueen = piece.upper() == "K" or piece.upper() == "Q"

        
    if not is_white or kingOrQueen:  # Check if king or queen is currently evaluated to correctly access mirrored PSQT
        return psqt[63 - field]  # Return mirrored value
    else:
         return psqt[field] # Else return 
        
        

# Return PSQT Table of piece
def getPsqtTable(piece, is_white):
    
    match piece.upper():
        case 'P': return constants.Psqt.PAWN_PSQT
        case 'R': return constants.Psqt.ROOK_PSQT
        case 'B': return constants.Psqt.BISHOP_PSQT
        case 'N': return constants.Psqt.KNIGHT_PSQT
        case 'Q': return getQueenPsqt(is_white)
        case 'K': return getKingPsqt(is_white)
        case _: logger.error(f"no PSQT found for {piece}"); return -1  



# Return white or black King-PSQT
def getKingPsqt(is_white):
    if is_white:
        return constants.Psqt.KING_PSQT
    else:
        return constants.Psqt.KING_PSQT_BLACK



# Return white or black Queen-PSQT
def getQueenPsqt(is_white):
    if is_white:
        return constants.Psqt.QUEEN_PSQT
    else:
        return constants.Psqt.QUEEN_PSQT_BLACK



# Returns 2D array of all possible moves for black and white in given position
# TODO Add Turn_object for en passent etc.
def generate_moves(fen):
    
    chessboard = fen_to_array(fen)
    moves = {} # Dic fpr all moves

    for i in range(8):
        for j in range(8):

            piece = chessboard[i][j]

            if piece == 0:
                continue
                

            if piece.isupper():

                match piece:
                    case 'P': moves.setdefault((i, j),[]).append(pawn_moves(i, j, True, chessboard))
                    case 'B': moves.setdefault((i, j),[]).append(bishop_moves(i, j, True, chessboard))
                    case 'N': moves.setdefault((i, j),[]).append(knight_moves(i, j, True, chessboard))
                    case 'R': moves.setdefault((i, j),[]).append(rook_moves(i,  j, True, chessboard))
                    case 'Q': moves.setdefault((i, j),[]).append(queen_moves(i, j, True, chessboard))
                    case 'K': moves.setdefault((i, j),[]).append(king_moves(i, j, True, chessboard))

            else: 

                match piece:
                    case 'p': moves.setdefault((i, j),[]).append(pawn_moves(i, j, False, chessboard))
                    case 'b': moves.setdefault((i, j),[]).append(bishop_moves(i, j, False, chessboard))
                    case 'n': moves.setdefault((i, j),[]).append(knight_moves(i, j, False, chessboard))
                    case 'r': moves.setdefault((i, j),[]).append(rook_moves(i, j, False, chessboard))
                    case 'q': moves.setdefault((i, j),[]).append(queen_moves(i, j, False, chessboard))
                    case 'k': moves.setdefault((i, j),[]).append(king_moves(i, j, False, chessboard))

    return moves
     
 

# TODO en passent etc.
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

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):
                possible_moves.append((row, column))
                # Gegner blockiert weitere Bewegung

            #else: # Eigene Figur blockiert Bewegung
            #   logger.debug(f"Knight blocked by own piece {row}, {column}")

    return possible_moves


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
                logger.debug(chessboard[row][column])
                logger.debug(is_enemy(is_white, chessboard[row][column]))
                possible_moves.append((row, column))
                break  # Gegner blockiert weitere Bewegung

            else: # Eigene Figur blockiert Bewegung
                break

    return possible_moves
        
def king_moves(field_row, field_column, is_white, chessboard):
    
    move_pattern = constants.Piece_moves.King
    possible_moves = []

    for direction in move_pattern:
        row, column = field_row, field_column  # Startposition

        if in_bound(row + direction[0], column + direction[1]):

            row += direction[0] # directioion[0] stores vertical movement
            column += direction[1] # directioion[0] stores horizontal movement

            if chessboard[row][column] == 0:
                logger.debug(f"King can move to {row}, {column}")
                possible_moves.append((row, column))

            elif chessboard[row][column] != 0 and is_enemy(is_white, chessboard[row][column]):
                possible_moves.append((row, column))
                logger.debug(f"King can capture {row}, {column}")
                  # Gegner blockiert weitere Bewegung

            else: # Eigene Figur blockiert Bewegung
                logger.debug(f"King blocked by own piece {row}, {column}")
                

    return possible_moves
        
        
def in_bound(row, column):
    return 0 <= row <= 7 and 0 <= column <= 7 


def is_enemy(is_white, figure):
    return str.islower(figure) if is_white else str.isupper(figure)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
