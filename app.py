from flask import Flask, jsonify, request
from services.items import get_items
from services.items import add_item
from services.prompt_process import process_text, process_text_with_model

app = Flask(__name__)


# Route: Fetch all items
@app.route('/items', methods=['GET'])
def fetch_items():
    result, status_code = get_items()
    return jsonify(result), status_code


# Route: Add a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    result, status_code = add_item(data)
    return jsonify(result), status_code


@app.route('/process-prompt', methods=['POST'])
def process_prompt():
    data = request.json
    result, status_code = process_text(data)
    return jsonify(result), status_code


@app.route('/process-prompt-model', methods=['POST'])
def process_prompt_model():
    data = request.json
    result, status_code = process_text_with_model(data)
    return jsonify(result), status_code


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
