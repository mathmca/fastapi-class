import pytest
from fastapi import status

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    for post in res.json():
        schemas.PostOut(**post)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/123456")

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Posts.id == test_posts[0].id
    assert post.Posts.content == test_posts[0].content
    assert post.Posts.title == test_posts[0].title
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
        ("new post", "new content", False),
        ("anotherpost", "1moreCONTENT", True),
        ("LastPost", "LastContent", False)
    ])
def test_creating_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.user_id == test_user['id']


def test_unauthorized_create_post(client):
    res = client.post("/posts/", json={"title": "title", "content": "content"})

    assert res.status_code == 401
    

def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401


def test_authorized_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204


def test_delete_none_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/918237")
    
    assert res.status_code == 404

# def test_delete_other_userpost():
# Test if another user can delete other users posts
def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[1].id}",
                                   json={"title": "updated_title", "content": "content"})
    updated_post = schemas.Post(**res.json())
    
    assert res.status_code == 200
    assert updated_post.title == "updated_title"
    assert updated_post.content == "content"

# def test_update_other_userpost():
# Test if another user can update other users posts
def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401


def test_update_none_post(authorized_client, test_posts, test_user):
    res = authorized_client.put("/posts/918237",
                                json={"title": "updated_title", "content": "content"})
    
    assert res.status_code == 404