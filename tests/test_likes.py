import pytest
from app import models


@pytest.fixture
def test_like(test_posts, session, test_user):
    new_like = models.Likes(posts_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()

def test_like_on_post(authorized_client, test_posts):
    res = authorized_client.post("/likes/", json={"post_id": test_posts[0].id,
                                                  "dir": 1})
    
    assert res.status_code == 201


def test_like_twice(authorized_client, test_posts, test_like):
    res = authorized_client.post("/likes/", json={"post_id": test_posts[0].id,
                                                  "dir": 1})
    
    assert res.status_code == 409

def test_delete_like(authorized_client, test_posts, test_like):
    res = authorized_client.post("/likes/", json={"post_id": test_posts[0].id,
                                                  "dir": 0})
    
    assert res.status_code == 201

def test_delete_unexisted_like(authorized_client, test_posts):
    res = authorized_client.post("/likes/", json={"post_id": 587723009,
                                                  "dir": 0})
    
    assert res.status_code == 404


def test_like_unauthorized_user(client, test_posts):
    res = client.post("/likes/", json={"post_id": test_posts[0].id,
                                                  "dir": 1})
    
    assert res.status_code == 401


def test_like_unexisted_post(authorized_client, test_posts):
    res = authorized_client.post("/likes/", json={"post_id": 80000,
                                                  "dir": 1})
    
    assert res.status_code == 404