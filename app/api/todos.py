from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Todo
from ..schemas import TodoSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


bp = Blueprint('todos', __name__)


@bp.route('/', methods=['GET'])
@jwt_required()
def list_todos():
    # getting user's id from jwt
    user_id = int(get_jwt_identity())

    # getting list of user's todos
    todos = Todo.query.filter_by(owner_id=user_id).order_by(Todo.created_at.desc()).all()

    # outputting nothig if no todos exist
    if not todos:
        return jsonify({"msg": "nothing to display"})

    # outputting result via schema
    return TodoSchema(many=True).dump(todos), 200


@bp.route('/', methods=['POST'])
@jwt_required()
def create_todo():
    # getting user's id from jwt
    user_id = int(get_jwt_identity())

    # getting data from json
    data = request.get_json() or {}

    # creating a new todo via schema
    schema = TodoSchema(session=db.session)
    obj = schema.load({**data, 'owner_id': user_id})

    # uploading new todo in database
    db.session.add(obj)
    db.session.commit()

    # outputting results
    return schema.dump(obj), 201


@bp.route('/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id: int):
    # getting user's id from jwt
    user_id = int(get_jwt_identity())

    # fingding required todo by its id
    todo = Todo.query.filter_by(id=todo_id, owner_id=user_id).first_or_404()

    # outputting results via schema
    return TodoSchema().dump(todo), 200


@bp.route('/<int:todo_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_todo(todo_id: int):
    # getting user's id from jwt
    user_id = int(get_jwt_identity())

    # fingding required todo by its id
    todo = Todo.query.filter_by(id=todo_id, owner_id=user_id).first_or_404()

    # getting data from json 
    data = request.get_json() or {}

    # changing todo according to data from json
    for k, v in data.items():
        if hasattr(todo, k):
            setattr(todo, k, v)
    
    # updating todo in db
    db.session.commit()

    # outputting results
    return TodoSchema().dump(todo), 200


@bp.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id: int):
    # getting user's id from jwt
    user_id = int(get_jwt_identity())

    # fingding required todo by its id
    todo = Todo.query.filter_by(id=todo_id, owner_id=user_id).first_or_404()

    # deleting todo and updating db
    db.session.delete(todo)
    db.session.commit()

    # outputting results
    return '', 204