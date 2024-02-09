from flask import Blueprint, request, jsonify
from db import db, User, Todo, create
from collections import OrderedDict

todos_bp = Blueprint('todos', __name__, url_prefix='/todos')


@todos_bp.route('/create-todos/', methods=['POST'])
def create_todo():
    data = request.json

    user_id = data.get('user_id')
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()
        return jsonify({"error": "User not found"}), 404

    todo_data = {
        "title": data.get('title'),
        "description": data.get('description'),
        "due_date": data.get('due_date'),
        "completed": data.get('completed'),
        "user": user
    }
    todo = Todo(**todo_data)
    create(db, todo)
    return jsonify({"message": "Todo created successfully...", "todo_id": todo.id})


def todos_serializer(todo):
    return OrderedDict([
        ("todo id", todo.id),
        ("todo user", todo.user_id),
        ("todo title", todo.title),
        ("todo description", todo.description),
        ("todo due date", todo.due_date),
        ("completed", todo.completed)
    ])


@todos_bp.route('/all/', methods=['GET'])
def show_todos():
    todos = db.query(Todo).all()
    serialize = [todos_serializer(todo) for todo in todos]
    return [serialize]


@todos_bp.route('/status-update/<todo_id>/', methods=['PATCH'])
def mark_complete(todo_id: int):
    update_status = request.json
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        for key, value in update_status.items():
            setattr(todo, key, value)
        db.commit()
        return jsonify({"message": f"Todo status with ID {todo_id} updated successfully"})
    else:
        return jsonify({"message": f"Todo status with ID {todo_id} not found"})

# print(show_todos())
