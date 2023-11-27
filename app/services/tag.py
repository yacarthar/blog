from typing import Union

from app.models import Tag


def get_tag_by_name(tag_name) -> Union[Tag, None]:
    return Tag.find_by_name(tag_name)


def create_tag(tag_name) -> Tag:
    tag = Tag.find_by_name(tag_name)
    if tag:
        return tag
    else:
        new_tag = Tag(name=tag_name)
        new_tag.save()
        new_tag.refresh()
        return new_tag
