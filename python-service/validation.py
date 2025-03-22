from flask import Flask, request, jsonify
from enum import IntEnum
import urllib.parse
import json

app = Flask(__name__)


class Pieces(IntEnum):
    Q = 950
    R= 400
    B = 300
    K = 300
    P = 100



@app.route('/best-move', methods=['POST'])
def getBestMove():
    
    
    data = request.get_json()

    print(data)

    received_fen = data["fen"]  # String has to be decoded -> String recieved as Bytes
    formatted_fen = urllib.parse.unquote(received_fen) # Return to ASCII-notation of FEN

    value = calcPieceValue(formatted_fen, data["turn"] == "white") # Calc current piece value of AIs pieces

    return value  




def calcPieceValue(fem, whites_turn): # TODO incremental 

    value = 0

    if whites_turn: # Calc Value based on upper chars
        for char in fem:
            if char == '+':
                break
            elif char.isupper():
                value += getattr(Pieces, char, 0)
            
    else: # Calc Value based on lower chars
         for char in fem: 
            if char == '+':
                break
            elif char.islower():
                value += getattr(Pieces, char.upper(), 0)
        
    
    return str(value)





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
