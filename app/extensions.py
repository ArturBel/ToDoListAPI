from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from marshmallow import Schema
import redis
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", '6379')
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Optionally configure marshmallow utils here
from flask_marshmallow import Marshmallow
ma = Marshmallow()