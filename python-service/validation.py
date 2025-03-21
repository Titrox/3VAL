from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/best-move', methods=['POST'])
def getBestMove():
    return "AIs turn"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
