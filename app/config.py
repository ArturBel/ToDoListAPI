import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# expirations
ACCESS_EXPIRY_MINUTES = int(os.getenv("ACCESS_EXPIRY_MINUTES", "1"))
REFRESH_EXPIRY_DAYS = int(os.getenv("REFRESH_EXPIRY_DAYS", "1"))

class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "extra-insecure-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=ACCESS_EXPIRY_MINUTES)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=REFRESH_EXPIRY_DAYS)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")