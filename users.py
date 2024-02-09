import bcrypt
from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from db import User, db, create
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


class CreateUser(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str


@users_bp.route('/register/', methods=['POST'])
def register():
    user_data = request.json
    user = CreateUser(**user_data)

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(username=user.username, password=hashed_password,
                   first_name=user.firstname, last_name=user.lastname)

    try:
        create(db, db_user)
        serialized_user = {"id": db_user.id, "username": db_user.username}
        return jsonify({"message": "User created successfully", "user": serialized_user})
    except IntegrityError as e:
        db.rollback()
        error_info = e.orig.args
        if "Duplicate entry" in str(error_info):
            return jsonify({"error": "Username already exists"}), 400
        else:
            return jsonify({"error": f"An error occurred while creating the user: {e}"}), 500
    finally:
        db.close()


def serialize_user(user):
    return {"id": user.id, "username": user.username}


@users_bp.route('/user/<user_id>/', methods=['GET'])
def get_users_with_id(user_id):
    try:
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            return jsonify({"user": serialize_user(user)} if user else {"message": "User not found"})
    finally:
        db.close()


@users_bp.route('/all/', methods=['GET'])
def get_all():
    users = db.query(User).all()
    serialize_users = [serialize_user(user) for user in users]
    return {"users": serialize_users}


def get_all_serializer(user):
    return {"id": user.id,
            "username": user.username,
            "first name": user.first_name,
            "last name": user.last_name}


@users_bp.route('/all/d/', methods=['GET'])
def get_all_detail():
    users = db.query(User).all()
    serialize_users = [get_all_serializer(user) for user in users]
    return serialize_users


@users_bp.route('/delete-user/<user_id>/', methods=['DELETE'])
def delete_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    db.close()
    return jsonify({"message": "user is deleted....!!!"})


@users_bp.route('/update/<user_id>/', methods=['PATCH'])
def update_user(user_id: int):
    update_user_data = request.json
    user = db.query(User).filter(User.id == user_id).first()
    # CHECK USER EXISTING
    if user:
        # update user object with new data
        for key, value in update_user_data.items():
            setattr(user, key, value)
        db.commit()
        return jsonify({"message": f"User with ID {user_id} updated successfully"})
    else:
        return jsonify({"message": f"User with ID {user_id} not found"})
