from typing import Union

from flask_sqlalchemy.pagination import SelectPagination

from app.models import Post, Tag
from app.services.category import get_category_by_name
from app.services.tag import get_tag_by_name


def list_post(page=1) -> SelectPagination:
    page_posts = Post.query.order_by(Post.date_created.desc()).paginate(
        page=page, per_page=5
    )
    return page_posts


def create_post(**kwargs) -> Union[Post, None]:
    new_post = Post(**kwargs)
    new_post.save()
    return new_post


def get_post(post_id) -> Union[Post, None]:
    post = Post.find_by_id(post_id)
    return post


def find_post_by_category(cat_name, page) -> SelectPagination:
    category = get_category_by_name(cat_name=cat_name)
    page = (
        Post.query.filter_by(category_id=category.id)
        .order_by(Post.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return page


def find_post_by_tag(tag_name, page) -> SelectPagination:
    tag = get_tag_by_name(tag_name=tag_name)
    page = (
        Post.query.join("tags")
        .filter(Tag.id == tag.id)
        .order_by(Post.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return page
