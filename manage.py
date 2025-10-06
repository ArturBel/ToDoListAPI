from app import create_app
from app.config import Config


app = create_app(config=Config)


if __name__ == '__main__':
    app.run()