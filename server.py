from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
import uuid
from datetime import timedelta

# Import database reference
from database.models import db

# Import services
from services.predict_attributes import get_attributes
from services.predict_clothing_items import predict
import services.utill as util_service
from services.color_recommend import apply_recommended_colors

# Import request validators
import validation.validations as validators

# Import controllers
import controllers.auth as auth_controller
import controllers.clothing_item as clothing_controller

# Import prompt processes
from services.prompt_process import predict_intent, get_response, fallback

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for now

# Database configuration
file_path = os.path.abspath(os.getcwd()) + '/database/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for JWT (Change this in production!)
app.config["JWT_SECRET_KEY"] = "closit_SECRET"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=17)

# Init db and jwt
db.init_app(app)
jwt = JWTManager(app)

this_dir = os.path.dirname(__file__)


# Routes
@app.route("/api/register/verify", methods=["POST"])
def register_user_verify():
    data = request.json
    # Validate request body against schema data types
    if data['email'] == "":
        return jsonify({'error': 'email not provided'}), 400

    # Check if username or email already exists
    if auth_controller.check_user_exists_by_email(data['email']):
        return jsonify({'error': 'Already exists'}), 400
    else:
        return jsonify({'message': 'No user found'}), 200


@app.route("/api/register", methods=["POST"])
def register_new_user():
    data = request.json
    # get validation schema
    schema = validators.NewUserSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400
    try:
        # Check if username or email already exists
        if auth_controller.check_user_exists_by_email(data['email']):
            return jsonify({'error': 'Already exists'}), 400
        # Create a new user
        new_user = auth_controller.save_new_user(data)
        return jsonify({'message': 'Registration successful', 'data': {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name
        }}), 201
    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


@app.route("/api/login", methods=["POST"])
def user_login():
    data = request.json
    # get validation schema
    schema = validators.UserLoginSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400

    try:
        # fetch the user
        user = auth_controller.check_user_exists_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid account email'}), 401
        # Verify password
        if not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid password'}), 401
        # if password match generate access token
        access_token = create_access_token(identity=str(data['email']))
        # assign access token to user
        user.accessToken = access_token
        db.session.commit()
        return jsonify({'message': 'login successful', 'accessToken': access_token}), 200
    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


@app.route("/api/forget-password", methods=["POST"])
def send_password_rest_email():
    data = request.json
    # get validation schema
    schema = validators.ForgetPasswordSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400

    try:
        # fetch the user
        user = auth_controller.check_user_exists_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid account email'}), 401
        # Generate reset token
        token = uuid.uuid4().hex
        # assign access token to user and save
        user.resetToken = token
        db.session.commit()
        # @TODO send password reset email with a token
        return jsonify({'message': 'Password reset email send'}), 201

    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


@app.route("/api/reset-password", methods=["POST"])
def rest_user_password():
    data = request.json
    # get validation schema
    schema = validators.ResetPasswordSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400
    try:
        # fetch the user
        user = auth_controller.check_user_exists_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid account email'}), 401
        # Check reset token
        if not user.resetToken == data['token']:
            return jsonify({'error': 'Invalid email or token'}), 403
        # update user password to new one
        user.password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify({'message': 'Password rest successful'}), 201

    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


@app.route("/api/me", methods=["GET"])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    try:
        # fetch the user
        user = auth_controller.check_user_exists_by_email(current_user)
        if not user:
            return jsonify({'error': 'Invalid token data'}), 400
        return jsonify({'message': 'user found', 'data': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }}), 201
    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


@app.route("/api/clothing-item", methods=["POST"])
@jwt_required()
def save_user_clothing_items():
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    data = request.json
    # get validation schema
    schema = validators.ClothingItemSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400

    try:
        # fetch the user
        user = auth_controller.check_user_exists_by_email(current_user)
        if not user:
            return jsonify({'error': 'Invalid token data'}), 400

        # fetch the clothing items of user
        clothing_items = clothing_controller.get_all_clothing_items_by_user(user.id)
        if len(clothing_items) > 0:
            for clothingItem in clothing_items:
                if (clothingItem.category == data['category']) and (clothingItem.colorCode == data['colorCode']) and (
                        clothingItem.material == data['material']):
                    return jsonify({'error': 'Already exists clothing item'}), 400

        # get clothing attributes
        clothing_attributes = get_attributes(data['category'], data['colorCode'], data['material'])

        # Create a new clothing item
        new_clothing_item = clothing_controller.save_new_clothing_item(data, user.id, clothing_attributes)
        # update dress code rules with new combinations
        util_service.update_dress_code_rules({
            'dressCodes': clothing_attributes['Dress_Codes'],
            'occasions': clothing_attributes['Occasions']
        })

        return jsonify({'message': 'Clothing item save successfully', 'data': {
            'id': new_clothing_item.id,
            'category': new_clothing_item.category,
            'colorCode': new_clothing_item.colorCode,
            'material': new_clothing_item.material,
            'clothing_attributes': clothing_attributes
        }}), 201
    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


@app.route("/api/clothing-item/<item>", methods=["GET"])
@jwt_required()
def get_clothing_item_by_id(item):
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    try:
        # fetch the clothing item
        clothing_item = clothing_controller.get_clothing_item_by_id(item)
        if not clothing_item:
            return jsonify({'error': 'Invalid clothing item'}), 400
        # fetch the clothing item dress codes
        clothing_item_dress_codes = clothing_controller.get_all_dress_codes_by_clothing_id(item)
        # fetch the clothing item occasions
        clothing_item_occasions = clothing_controller.get_all_occasions_by_clothing_id(item)
        # fetch the clothing item weathers
        clothing_item_weathers = clothing_controller.get_all_weather_conditions_by_clothing_id(item)

        # create dress code array
        clothing_item_dress_codes_array = [dc.dressCode for dc in clothing_item_dress_codes]
        # create occasion array
        clothing_item_occasions_array = [oc.occasion for oc in clothing_item_occasions]
        # create weather array
        clothing_item_weather_array = [w.weather for w in clothing_item_weathers]

        return jsonify({'message': 'Clothing item found', 'data': {
            'id': clothing_item.id,
            'category': clothing_item.category,
            'colorCode': clothing_item.colorCode,
            'material': clothing_item.material,
            'dressCodes': clothing_item_dress_codes_array,
            'occasions': clothing_item_occasions_array,
            'weather': clothing_item_weather_array
        }}), 200
    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


@app.route("/api/clothing-item/user", methods=["GET"])
@jwt_required()
def get_clothing_items_of_login_user():
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    try:
        # fetch the user
        user = auth_controller.check_user_exists_by_email(current_user)
        if not user:
            return jsonify({'error': 'Invalid token data'}), 400

        clothing_items_array = clothing_controller.get_user_wardrobe(user.id)

        return jsonify({'message': 'Clothing items found', 'data': clothing_items_array}), 200
    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


@app.route("/api/recommendation", methods=["POST"])
@jwt_required()
def get_clothing_item_recommendations():
    data = request.json
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    try:
        # fetch the user
        user = auth_controller.check_user_exists_by_email(current_user)
        if not user:
            return jsonify({'error': 'Invalid token data'}), 400
        # get user prompt
        prompt = data.get("prompt", "")

        # Predict tag first
        intent_tag = predict_intent(prompt)

        if intent_tag != "unknown":
            # Intent matched, return the intent response
            response = get_response(intent_tag)
            return jsonify({'message': response}), 200
        else:
            # get clothing recommendation based on prompt
            clothing_recommendations = predict(prompt)

            if not clothing_recommendations["predicted_dress_codes"] and not clothing_recommendations["predicted_clothing_items"]:
                # No clothing prediction either, now return fallback
                response = fallback()
                return jsonify({'message': response}), 200
            else:
                # get user wardrobe items
                user_clothing_items_array = clothing_controller.get_user_wardrobe(user.id)
                # create filters for recommendation mapping
                filters = {
                    'dress_codes': clothing_recommendations["predicted_dress_codes"],
                    'occasions': clothing_recommendations["extracted_info"]["occasions"],
                    'weather': [],
                    'colors': clothing_recommendations["extracted_info"]["colors"]
                }
                # match recommendations to wardrobe items
                matched, missing = clothing_controller.match_recommendations_to_wardrobe(user_clothing_items_array, clothing_recommendations["predicted_clothing_items"], filters)
                # format missing items to objects
                missing_obj = util_service.create_missing_clothing_items_obj(missing, filters)
                # get color recommendations for missing items
                missing_with_color = apply_recommended_colors(missing_obj)
                return jsonify({'data': {
                    "matched": matched,
                    "missing": missing_with_color
                }}), 200
    except SQLAlchemyError as e:
        return util_service.sql_alchemy_error_handlers(e)
    except Exception as e:
        return util_service.exception_handlers(e)


# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3030, debug=True)
