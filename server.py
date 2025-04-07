import requests
import json
from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import and_, PrimaryKeyConstraint
from sqlalchemy.testing.suite.test_reflection import users
from werkzeug.security import generate_password_hash, check_password_hash
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
import logging
from flask import jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from validation.validations import NewUserSchema, UserLoginSchema, ForgetPasswordSchema, ResetPasswordSchema, ClothingItemSchema
from marshmallow import Schema, fields, ValidationError, validate
import uuid
from datetime import timedelta

from services.predict_attributes import get_attributes
from services.predict_clothing_items import predict

# Initialize Flask app
app = Flask(__name__)
# enable logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for now
# Database configuration
file_path = os.path.abspath(os.getcwd()) + '/database/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Secret key for JWT (Change this in production!)
app.config["JWT_SECRET_KEY"] = "closit_SECRET"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=17)
jwt = JWTManager(app)


# Define Models
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    accessToken = db.Column(db.String(255), nullable=True)
    resetToken = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    # Relationships
    clothingItem = db.relationship('ClothingItem', backref='users', uselist=False)

class ClothingItem(db.Model):
    __tablename__ = 'clothingItem'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    colorCode = db.Column(db.String(50), nullable=False)
    material = db.Column(db.String(50), nullable=False)
    createdAt = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    # Relationships
    clothingItemDressCodes = db.relationship('ClothingItemDressCode', backref='ClothingItem')
    clothingItemOccasions = db.relationship('ClothingItemOccasion', backref='ClothingItem')
    clothingItemWeather = db.relationship('ClothingItemWeather', backref='ClothingItem')

class ClothingItemDressCode(db.Model):
    __tablename__ = 'clothingItemDressCode'
    clothingItemId = db.Column(db.Integer, db.ForeignKey('clothingItem.id'), nullable=False, primary_key=True)
    dressCode = db.Column(db.String(50), nullable=False, primary_key=True)

class ClothingItemOccasion(db.Model):
    __tablename__ = 'clothingItemOccasion'
    clothingItemId = db.Column(db.Integer, db.ForeignKey('clothingItem.id'), nullable=False, primary_key=True)
    occasion = db.Column(db.String(255), nullable=False, primary_key=True)

class ClothingItemWeather(db.Model):
    __tablename__ = 'clothingItemWeather'
    clothingItemId = db.Column(db.Integer, db.ForeignKey('clothingItem.id'), nullable=False, primary_key=True)
    weather = db.Column(db.String(100), nullable=False, primary_key=True)

# error handlers
def sql_alchemy_error_handlers(e):
    db.session.rollback()
    app.logger.error(f"Database error: {str(e)}")
    return jsonify({'error': 'Database error'}), 500

def exception_handlers(e):
    app.logger.error(f"Unexpected error: {str(e)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500
# Routes
@app.route("/api/register/verify", methods=["POST"])
def register_user_verify():
    data = request.json
    # Validate request body against schema data types
    if data['email'] == "":
        return jsonify({'error': 'email not provided'}), 400

    # Check if username or email already exists
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Already exists'}), 400
    else:
        return jsonify({'message': 'No user found'}), 200


@app.route("/api/register", methods=["POST"])
def register_new_user():
    data = request.json
    # get validation schema
    schema = NewUserSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400

    # Check if username or email already exists
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Already exists'}), 400

    try:
        # Create a new user
        new_user = Users(
            email=data['email'],
            name=data['name'],
            password=generate_password_hash(data['password']),  # Hash the password
        )
        db.session.add(new_user)
        # Flush to get the new User
        db.session.flush()
        # Commit changes to the database
        db.session.commit()
        return jsonify({'message': 'Registration successful', 'data': {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name
        }}), 201
    except SQLAlchemyError as e:
        sql_alchemy_error_handlers(e)
    except Exception as e:
        exception_handlers(e)

@app.route("/api/login", methods=["POST"])
def user_login():
    data = request.json
    # get validation schema
    schema = UserLoginSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400

    try:
        # fetch the user
        user = Users.query.filter_by(email=data['email']).first()
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
        sql_alchemy_error_handlers(e)
    except Exception as e:
        exception_handlers(e)

@app.route("/api/forget-password", methods=["POST"])
def send_password_rest_email():
    data = request.json
    # get validation schema
    schema = ForgetPasswordSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400

    try:
        # fetch the user
        user = Users.query.filter_by(email=data['email']).first()
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
        sql_alchemy_error_handlers(e)
    except Exception as e:
        exception_handlers(e)

@app.route("/api/reset-password", methods=["POST"])
def rest_user_password():
    data = request.json
    # get validation schema
    schema = ResetPasswordSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400
    try:
        # fetch the user
        user = Users.query.filter_by(email=data['email']).first()
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
        sql_alchemy_error_handlers(e)
    except Exception as e:
        exception_handlers(e)

@app.route("/api/me", methods=["GET"])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    try:
        # fetch the user
        user = Users.query.filter_by(email=current_user).first()
        if not user:
            return jsonify({'error': 'Invalid token data'}), 400
        return jsonify({'message': 'user found', 'data': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }}), 201
    except SQLAlchemyError as e:
        sql_alchemy_error_handlers(e)
    except Exception as e:
        exception_handlers(e)

@app.route("/api/clothing-item", methods=["POST"])
@jwt_required()
def save_user_clothing_items():
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    data = request.json
    # get validation schema
    schema = ClothingItemSchema()
    # Validate request body against schema data types
    try:
        schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify({"error": err.messages}), 400

    try:
        # fetch the user
        user = Users.query.filter_by(email=current_user).first()
        if not user:
            return jsonify({'error': 'Invalid token data'}), 400

        # fetch the clothing items of user
        clothing_items = ClothingItem.query.filter_by(userId=user.id).all()
        if len(clothing_items) > 0:
            for clothingItem in clothing_items:
                if (clothingItem.category == data['category']) and (clothingItem.colorCode == data['colorCode']) and (clothingItem.material == data['material']):
                    return jsonify({'error': 'Already exists clothing item'}), 400

        # get clothing attributes
        clothing_attributes = get_attributes(data['category'], data['colorCode'], data['material'])

        # Create a new clothing item
        new_clothing_item = ClothingItem(
            userId=user.id,
            category=data['category'],
            colorCode=data['colorCode'],
            material=data['material']
        )
        db.session.add(new_clothing_item)
        # Flush to get the new User
        db.session.flush()

        if new_clothing_item.id:
            # create clothing item dress codes
            for dressCode in clothing_attributes['Dress_Codes']:
                db.session.add(
                    ClothingItemDressCode(
                        clothingItemId=new_clothing_item.id,
                        dressCode=dressCode
                    )
                )
                db.session.flush()
            # create clothing item occasions
            for occasion in clothing_attributes['Occasions']:
                db.session.add(
                    ClothingItemOccasion(
                        clothingItemId=new_clothing_item.id,
                        occasion=occasion
                    )
                )
                db.session.flush()
            # create clothing item weather
            for weather in clothing_attributes['Weather_Conditions']:
                db.session.add(
                    ClothingItemWeather(
                        clothingItemId=new_clothing_item.id,
                        weather=weather
                    )
                )
                db.session.flush()
        # Commit changes to the database
        db.session.commit()
        return jsonify({'message': 'Clothing item save successfully', 'data': {
            'id': new_clothing_item.id,
            'category': new_clothing_item.category,
            'colorCode': new_clothing_item.colorCode,
            'material': new_clothing_item.material,
            'clothing_attributes': clothing_attributes
        }}), 201
    except SQLAlchemyError as e:
        return sql_alchemy_error_handlers(e)
    except Exception as e:
        return exception_handlers(e)

@app.route("/api/clothing-item/<item>", methods=["GET"])
@jwt_required()
def get_clothing_item_by_id(item):
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    try:
        # fetch the clothing item
        clothing_item = ClothingItem.query.filter_by(id=item).first()
        if not clothing_item:
            return jsonify({'error': 'Invalid clothing item'}), 400
        # fetch the clothing item dress codes
        clothing_item_dress_codes = ClothingItemDressCode.query.filter_by(clothingItemId=item).all()
        # fetch the clothing item occasions
        clothing_item_occasions = ClothingItemOccasion.query.filter_by(clothingItemId=item).all()
        # fetch the clothing item weathers
        clothing_item_weathers = ClothingItemWeather.query.filter_by(clothingItemId=item).all()

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
        return sql_alchemy_error_handlers(e)
    except Exception as e:
        return exception_handlers(e)

@app.route("/api/clothing-item/user", methods=["GET"])
@jwt_required()
def get_clothing_items_of_login_user():
    current_user = get_jwt_identity()
    # Validate JWT data
    if not current_user:
        return jsonify({"error": "Invalid token data"}), 400

    try:
        # fetch the user
        user = Users.query.filter_by(email=current_user).first()
        if not user:
            return jsonify({'error': 'Invalid token data'}), 400
        # fetch the clothing items of user
        clothing_items = ClothingItem.query.filter_by(userId=user.id).all()
        if len(clothing_items) <= 0:
            return jsonify({'message': 'No clothing item saved yet', 'data': []}), 200

        clothing_items_array = []
        for clothingItem in clothing_items:
            # fetch the clothing item dress codes
            clothing_item_dress_codes = ClothingItemDressCode.query.filter_by(clothingItemId=clothingItem.id).all()
            # fetch the clothing item occasions
            clothing_item_occasions = ClothingItemOccasion.query.filter_by(clothingItemId=clothingItem.id).all()
            # fetch the clothing item weathers
            clothing_item_weathers = ClothingItemWeather.query.filter_by(clothingItemId=clothingItem.id).all()
            # create dress code array
            clothing_item_dress_codes_array = [dc.dressCode for dc in clothing_item_dress_codes]
            # create occasion array
            clothing_item_occasions_array = [oc.occasion for oc in clothing_item_occasions]
            # create weather array
            clothing_item_weather_array = [w.weather for w in clothing_item_weathers]
            clothing_items_array.append(
                {
                    'id': clothingItem.id,
                    'userId': clothingItem.userId,
                    'category': clothingItem.category,
                    'colorCode': clothingItem.colorCode,
                    'material': clothingItem.material,
                    'dressCodes': clothing_item_dress_codes_array,
                    'occasions': clothing_item_occasions_array,
                    'weather': clothing_item_weather_array
                }
            )
        return jsonify({'message': 'Clothing items found', 'data': clothing_items_array}), 200
    except SQLAlchemyError as e:
        return sql_alchemy_error_handlers(e)
    except Exception as e:
        return exception_handlers(e)

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
        user = Users.query.filter_by(email=current_user).first()
        if not user:
            return jsonify({'error': 'Invalid token data'}), 400

        clothing_recommendations = predict(data["prompt"])
        print(clothing_recommendations)
        return jsonify({'message': 'Clothing items found', 'data': clothing_recommendations}), 200
    except SQLAlchemyError as e:
        return sql_alchemy_error_handlers(e)
    except Exception as e:
        return exception_handlers(e)

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3030, debug=True)
