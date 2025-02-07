from flask import Flask, jsonify, request
from services.items import get_items, add_item, create_tables
from services.prompt_process import (process_text, process_text_with_model,
                                     process_text_with_multi_data_model, predict_all)
from services.color_process import get_matching_colors

app = Flask(__name__)


@app.route('/create', methods=['GET'])
def create_data_tables():
    result, status_code = create_tables()
    return jsonify(result), status_code


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


@app.route('/process-prompt-multi-data-model', methods=['POST'])
def process_prompt_multi_data_model():
    data = request.json
    result, status_code = process_text_with_multi_data_model(data)
    return jsonify(result), status_code


@app.route('/predictAll', methods=['POST'])
def predict_with_all_models():
    data = request.get_json()
    result = predict_all(data)
    return jsonify(result)


@app.route('/getMatchingColors', methods=['POST'])
def get_color_matching():
    data = request.get_json()
    result = get_matching_colors(data)
    return jsonify(result)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
