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
    generate_moves(formatted_fen, is_white)
    return value  


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
        case 'Q': return getQueenPsqt(is_white)
        case 'R': return constants.Psqt.ROOK_PSQT
        case 'B': return constants.Psqt.BISHOP_PSQT
        case 'P': return constants.Psqt.PAWN_PSQT
        case 'N': return constants.Psqt.KNIGHT_PSQT
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



def generate_moves(fen, is_white):
    chessboard = fen_to_array(fen)

    for i in range(63):
        figure = chessboard[i]

        if figure.upper() == "P":
            return
        elif figure.upper() == "R":
            return
        elif figure.upper() == "N":
            return
        elif figure.upper() == "B":
            return
        elif figure.upper() == "K":
            return
        elif figure.upper() == "Q":
            return      
        
        
        


def fen_to_array(fen):
    
    chessboard = [0] * 64
    currentField = 0

    for char in fen: 
        if char.isalpha():
            chessboard[currentField] = char
            currentField += 1

        elif char.isdigit():
            currentField += int(char)

        elif char == " ":
            break

    return chessboard


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
