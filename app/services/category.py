from typing import Union

from app.models import Category


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
