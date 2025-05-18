from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import main as main
import training as training

model = "trained_model _BW_10000.pkl"

app = Flask(__name__)
CORS(app)  # Allow requests from JS (like http://localhost:5500)

@app.route('/call-python', methods=['POST'])
def call_python():
    data = request.json
    arg = data.get('arg', '')
    neural_network = training.Testing.load("trained_model _BW_10000.pkl")
    tester = training.Testing(neural_network)
    result = tester.attempt(arg)
    print(result)
    return jsonify({"message": f"Hello from Python! We send: {chr(65+result)}"})

if __name__ == '__main__':
    app.run(port=5000)
