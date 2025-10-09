from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    # getting data from json
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # checking if all fields are present
    if not username or not email or not password:
        return jsonify({'msg': 'username, email and password are required'}), 400

    # checking if username or email already taken
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'email already registred'}), 401
    elif User.query.filter_by(username=username).first():
        return jsonify({'msg': f'username "{username}" already taken'}), 401

    # creating a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    # adding new user to the database
    db.session.add(new_user)
    db.session.commit()

    # creating access and refresh tokens upon registration
    access_token = create_access_token(identity=str(new_user.id))
    refresh_token = create_refresh_token(identity=str(new_user.id))

    # outputing results
    return jsonify({'message': 'user registered successully', 
                    'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email,
                    'access_token': access_token,
                    "refresh_token": refresh_token}), 201


@bp.route('/login', methods=['POST'])
def login():
    # getting data from json
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    # checking if required fields are filled
    if not email or not password:
        return jsonify({'msg': 'email and password required'}), 400

    # checking if user exists and password is correct
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'invalid credentials'}), 401

    # creating access and refresh tokens upon login
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({'msg': 'login successful', 
                    'access_token': access_token,
                    'refresh_token': refresh_token}), 200


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # getting user's id from refresh token
    user_id = int(get_jwt_identity())

    # creating new access token and outputting it
    new_access_token = create_access_token(identity=str(user_id))
    return jsonify({"new_access_token": new_access_token}), 201