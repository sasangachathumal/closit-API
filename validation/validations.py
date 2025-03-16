from marshmallow import Schema, fields, ValidationError, validate

class NewUserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.String(required=True)
    password = fields.String(required=True, validate=[validate.Length(min=8)])

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class ForgetPasswordSchema(Schema):
    email = fields.Email(required=True)

class ResetPasswordSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[validate.Length(min=8)])
    token = fields.String(required=True)

class ClothingItemSchema(Schema):
    category = fields.String(required=True)
    colorCode = fields.String(required=True)
    material = fields.String(required=True)
