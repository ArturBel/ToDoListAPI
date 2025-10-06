from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from marshmallow import Schema

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Optionally configure marshmallow utils here
from flask_marshmallow import Marshmallow
ma = Marshmallow()