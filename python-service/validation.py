from flask import Flask, request, jsonify
from enum import IntEnum
import numpy as np
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

    received_fen = data["fen"]  # String has to be decoded -> String recieved as Bytes
    formatted_fen = urllib.parse.unquote(received_fen) # Return to ASCII-notation of FEN

    value = calcPieceValueWithPSQT(formatted_fen, data["turn"] == "white") # Calc current piece value of AIs pieces

    return value  


# TODO Need for whites_turn? Fix 

def calcPieceValueWithPSQT(fem, whites_turn): # TODO incremental 

    value = 0
    logger.debug(fem)
    currentField = 0

    for char in fem: 
        if char.isupper(): # White
            psqtValue = getPsqtValue(currentField, char, True)
            value += getattr(Pieces, char, 0) + psqtValue

            logger.debug(f"{char} : {getattr(Pieces, char, 0)} PSQRT: {psqtValue} Feld: {currentField} Value insgesamt: {getattr(Pieces, char, 0) + psqtValue}")
    
            currentField += 1 
        elif char.islower(): # Black
            psqtValue = getPsqtValue(currentField, char, False)
            value -= getattr(Pieces, char.upper(), 0) + psqtValue
            
            logger.debug(f"{char} : {getattr(Pieces, char.upper(), 0)} PSQRT: {psqtValue} Feld: {currentField} Value insgesamt: {getattr(Pieces, char.upper(), 0) + psqtValue}")
            
            currentField += 1
        elif char.isdigit():
            currentField += int(char)
        if char == ' ':
            break
            
        logger.debug(value)
    return str(value)



def getPsqtValue(field, piece, is_white):

    psqt = getPsqtTable(piece, is_white)

    if not is_white:
        return psqt[63 - field]  # Korrektes Spiegeln für 8x8 Brett]


    # logger.debug(psqt)
    return psqt[field]

    


def getPsqtTable(piece, is_white):
    
    match piece.upper():
        case 'Q': return getQueenPsqt(is_white)
        case 'R': return constants.Psqt.ROOK_PSQT
        case 'B': return constants.Psqt.BISHOP_PSQT
        case 'P': return constants.Psqt.PAWN_PSQT
        case 'N': return constants.Psqt.KNIGHT_PSQT
        case 'K': return getKingPsqt(is_white)
        case _: return -1  


def getKingPsqt(is_white):
    if is_white:
        return constants.Psqt.KING_PSQT
    else:
        return constants.Psqt.KING_PSQT_BLACK
    
def getQueenPsqt(is_white):
    if is_white:
        return constants.Psqt.QUEEN_PSQT
    else:
        return constants.Psqt.QUEEN_PSQT_BLACK

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
