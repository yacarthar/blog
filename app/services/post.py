from typing import Union
from app.models import PostModel


def list_post() -> Union[list[PostModel], None]:
    posts = PostModel.query.order_by(PostModel.date_created.desc()).all()
    return posts


def create_post(data) -> Union[PostModel, None]:
    new_post = PostModel(**data)
    new_post.save()
    return new_post


def get_post(post_id) -> Union[PostModel, None]:
    post = PostModel.find_by_id(post_id)
    return post
