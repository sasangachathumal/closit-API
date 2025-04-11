from werkzeug.security import generate_password_hash, check_password_hash
from database.models import db, Users

def check_user_exists_by_email(email):
    return Users.query.filter_by(email=email).first()

def save_new_user(data):
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
    return new_user
