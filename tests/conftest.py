from sqlalchemy import create_engine
from app.config import settings
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.oauth2 import create_access_token
import uuid
from app import models
from app.database import get_db, Base
from alembic import command

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.
    database_hostname}:{settings.database_port}/{settings.database_name}_test'
# we can also hardcode our url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Base.metadata.drop_all(bind=engine)
    # #run our code before we run our test these two are without alembic
    # Base.metadata.create_all(bind=engine)
    #command.upgrade("head")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    #run over code after our test finishes
    #command.downgrade("base") with alembic

@pytest.fixture
def test_user1(client):
    # user_data = {"email": "alim@gmail.com",
    #              "password": "password123"} # can be used with scope module
    user_data = {
    "email": f"test{uuid.uuid4()}@gmail.com",
    "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    # user_data = {"email": "alim@gmail.com",
    #              "password": "password123"} # can be used with scope module
    user_data = {
    "email": f"test{uuid.uuid4()}@gmail.com",
    "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    # user_data = {"email": "alim@gmail.com",
    #              "password": "password123"} # can be used with scope module
    user_data = {
    "email": f"test{uuid.uuid4()}@gmail.com",
    "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorize_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "1st title",
            "content": "i really liked it",
            "owner_id": test_user['id']
        },
        {
            "title": "2st title",
            "content": "i liked it",
            "owner_id": test_user['id']
        },
        {
            "title": "3st title",
            "content": "i should have liked it",
            "owner_id": test_user2['id']
        }]
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts) # we can hardcode all the values in add_all with models.Post
    session.commit()
    all_posts = session.query(models.Post).all()
    return all_posts