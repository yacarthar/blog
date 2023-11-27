from typing import Union

from app.models import Post


def list_post() -> Union[list, None]:
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return posts


def create_post(**kwargs) -> Union[Post, None]:
    new_post = Post(**kwargs)
    new_post.save()
    return new_post


def get_post(post_id) -> Union[Post, None]:
    post = Post.find_by_id(post_id)
    return post
