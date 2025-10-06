from flask import Blueprint
from .auth import bp as auth_bp
from .todos import bp as todos_bp


def register_api(app):
    api = Blueprint('api', __name__, url_prefix='/api')
    app.register_blueprint(api)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todos_bp, url_prefix='/api/todos')
