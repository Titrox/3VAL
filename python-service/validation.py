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
    logger.debug(generate_moves(formatted_fen, is_white))
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



# Returns array of all possible moves for one side in given position
def generate_moves(fen, is_white):
    
    chessboard = fen_to_array(fen)
    possible_moves = []

    for i in range(8):
        for j in range(8):

            piece = chessboard[i][j]

            if is_white:

                match piece:
                    case 'P': possible_moves.append(pawn_moves(i, j, is_white))
                    case 'B': possible_moves.append(bishop_moves(i, j, is_white))
                    case 'N': possible_moves.append(knight_moves(i, j, is_white))
                    case 'R': possible_moves.append(rook_moves(i,  j, is_white))
                    case 'Q': possible_moves.append(queen_moves(i, j, is_white))
                    case 'K': possible_moves.append(king_moves(i, j, is_white))

            else: 

                match piece:
                    case 'p': possible_moves.append(pawn_moves(i, j, is_white))
                    case 'b': possible_moves.append(bishop_moves(i, j, is_white))
                    case 'n': possible_moves.append(knight_moves(i, j, is_white))
                    case 'r': possible_moves.append(rook_moves(i, j, is_white))
                    case 'q': possible_moves.append(queen_moves(i, j, is_white))
                    case 'k': possible_moves.append(king_moves(i, j, is_white))

    return possible_moves

            
 
def pawn_moves(field_row, field_column, is_white):
    return f"pawn moves {field_row, field_column, is_white}"

def bishop_moves(field_row, field_column, is_white):
    return f"bishop move {field_row, field_column, is_white}"

def knight_moves(field_row, field_column, is_white):
    return f"knight move {field_row, field_column, is_white}"

def rook_moves(field_row, field_column, is_white):
    return f"rook move {field_row, field_column, is_white}"

def queen_moves(field_row, field_column, is_white):
    return f"queen move {field_row, field_column, is_white}"
        
def king_moves(field_row, field_column, is_white):
    return f"king move {field_row, field_column, is_white}"
        
        



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
