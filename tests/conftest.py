from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest

from app.main import app
from app.config import settings
from app.database import get_db, engine, Base
from app import models, schemas
from app.ouauth2 import create_access_token


# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip_adress/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    # Here we need to create multiple users to be used in:
    # 
    user_data = {
        "email": "hello123@gmail.com",
        "password": "pass123"
    }
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']

    assert res.status_code == 201
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "first_title",
            "content": "first_content",
            "user_id": test_user['id']
        }, {
            "title": "second_title",
            "content": "second_content",
            "user_id": test_user['id']
        }, {
            "title": "third_title",
            "content": "third_content",
            "user_id": test_user['id']
        }]

    def create_posts_model(posts):
        return models.Posts(**posts)

    post_map = map(create_posts_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Posts).all()

    return posts
    # Create a new post from another user for testing in posts
