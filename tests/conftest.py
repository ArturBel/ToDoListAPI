import pytest
from app import create_app
from app.config import TestConfig
from app.extensions import db


@pytest.fixture(scope='session')
def app():
    app = create_app(config=TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    yield
    # After each test, truncate all tables
    # (keeps schema but clears rows)
    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
