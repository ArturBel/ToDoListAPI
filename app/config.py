import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "extra-insecure-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")