from typing import Union
from app.models import Post


def list_post() -> Union[list[Post], None]:
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return posts


def create_post(data) -> Union[Post, None]:
    new_post = Post(**data)
    new_post.save()
    return new_post


def get_post(post_id) -> Union[Post, None]:
    post = Post.find_by_id(post_id)
    return post
