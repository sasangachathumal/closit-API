# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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

