from flask import Flask, request, jsonify
from flask_cors import CORS
import main as main
import training as training
import os

default_model = "trained_model_10000.pkl"

app = Flask(__name__)
CORS(app)  # Allow requests from JS (like http://localhost:5500)

def get_file_names(folder_path):
  file_names = []
  for item in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item)
    if os.path.isfile(item_path):
      file_names.append(item)
  return file_names

@app.route('/call-network', methods=['POST'])
def call_network():
    data = request.json
    arg = data.get('arg', '')
    model = data.get('model', default_model)
    model = default_model if model == "" else model
    print(f"Running on {model}")
    neural_network = training.Testing.load(f"models/{model}")
    tester = training.Testing(neural_network)
    result = tester.attempt(arg)
    print(result)
    return jsonify({"message": chr(65+result)})

@app.route('/call-files', methods=['POST'])
def call_files():
    data = request.json
    arg = data.get('arg', '')
    result = get_file_names("models")
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(port=5000)
