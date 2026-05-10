from typing import List
import pytest
from app import schems

def test_get_all_posts(authorize_client, test_posts):
    #client.post(login) # it is valid but we will not use this
    res = authorize_client.get("/posts/")
    def validate(post):
        return schems.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[2].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorize_client, test_posts):
    res = authorize_client.get(f"/posts/8888")
    assert res.status_code == 404

def test_get_one_valid_post(authorize_client, test_posts):
    res = authorize_client.get(f"/posts/{test_posts[0].id}")
    post = schems.PostOut(**res.json()) # it is to unpack it and get it in order
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published",[
    ("awesome title", "awesome content", True),
    ("amazing title", "amazing content", True),
    ("wounderful title", "wonderful content", False)
])
def test_create_post(authorize_client, test_user, test_posts, title, content, published):
    res = authorize_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schems.Post(**res.json())
    assert res.status_code  == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorize_client, test_user, test_posts):
    res = authorize_client.post("/posts/", json={"title": "arbitary", "content": "fisfskl"})

    created_post = schems.Post(**res.json())
    assert res.status_code  == 201
    assert created_post.title == "arbitary"
    assert created_post.content == "fisfskl"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorize_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitary", "content": "fisfskl"})
    assert res.status_code == 401

def test_unauthorize_user_deleting_post(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorize_client, test_posts, test_user):
    res = authorize_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_deleting_non_existent_post(authorize_client, test_posts, test_user):
    res = authorize_client.delete(f"/posts/9999")
    assert res.status_code == 404

def test_delete_other_user_post(authorize_client, test_posts, test_user):
    res = authorize_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403

def test_update_post(authorize_client, test_posts, test_user):
    data={
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorize_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schems.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_updating_other_user_post(authorize_client, test_posts, test_user):
    data={
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id
    }
    res = authorize_client.put(f"/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 403

def test_unauthorize_user_update_post(client, test_posts, test_user):
    data={
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id
    }
    res = client.put(f"/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 401

def test_updating_the_non_existent_post(authorize_client, test_posts, test_user):
    data={
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[1].id
    }
    res = authorize_client.put(f"/posts/9999", json=data)
    assert res.status_code == 404