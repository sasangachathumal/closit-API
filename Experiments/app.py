# from flask import Flask, jsonify, request
# from flask_jwt_extended import JWTManager
#
# # from services.items import get_items, add_item, create_tables
# from Experiments.prompt_process import (process_text, process_text_with_model,
#                                         process_text_with_multi_data_model, predict_all)
# from services.color_process import get_matching_colors
#
# # from routes.user_routes import user_routes_bp
#
# app = Flask(__name__)
#
# # Secret key for JWT (Change this in production!)
# app.config["JWT_SECRET_KEY"] = "clositAPI"
# jwt = JWTManager(app)
#
# # app.register_blueprint(user_routes_bp)
#
#
# @app.route('/process-prompt', methods=['POST'])
# def process_prompt():
#     data = request.json
#     result, status_code = process_text(data)
#     return jsonify(result), status_code
#
#
# @app.route('/process-prompt-model', methods=['POST'])
# def process_prompt_model():
#     data = request.json
#     result, status_code = process_text_with_model(data)
#     return jsonify(result), status_code
#
#
# @app.route('/process-prompt-multi-data-model', methods=['POST'])
# def process_prompt_multi_data_model():
#     data = request.json
#     result, status_code = process_text_with_multi_data_model(data)
#     return jsonify(result), status_code
#
#
# @app.route('/predictAll', methods=['POST'])
# def predict_with_all_models():
#     data = request.get_json()
#     result = predict_all(data)
#     return jsonify(result)
#
#
# @app.route('/getMatchingColors', methods=['POST'])
# def get_color_matching():
#     data = request.get_json()
#     result = get_matching_colors(data)
#     return jsonify(result)
#
#
# # Run the app
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=3035, debug=True)
