from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, ma
from .api import register_api
from .errors import register_error_handlers


def create_app(config=Config):
    # initializing app
    app = Flask(__name__, static_folder=None)

    # load configuration
    app.config.from_object(config)

    # initializing extensions
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app=app)
    ma.init_app(app=app)

    # registering blueprints and error handlers
    register_api(app=app)
    register_error_handlers(jwt=jwt)

    # health endpoint
    @app.route('/health')
    def health():
        return {"status": "okay"}, 200
    
    return app
