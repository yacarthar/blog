from typing import Union

from sqlalchemy import func

from app.models import Category, Post, db


def get_category_by_name(cat_name) -> Union[Category, None]:
    return Category.find_by_name(cat_name)


def create_category(name) -> Category:
    cat = Category.find_by_name(name)
    if cat:
        return cat
    else:
        new_cat = Category(name=name)
        new_cat.save()
        new_cat.refresh()
        return new_cat


def get_top_categories() -> list:
    top_categories = (
        db.session.query(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            func.count(Post.id).label("post_count"),
        )
        .join(Post, Category.id == Post.category_id)
        .group_by(Category.id, Category.name)
        .order_by(func.count(Post.id).desc())
        .limit(10)
        .all()
    )
    return top_categories
