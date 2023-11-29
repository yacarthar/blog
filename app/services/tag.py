from typing import Union

from sqlalchemy import func

from app.models import Tag, db, post_x_tag


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


def get_top_tags() -> list:
    top_tags = (
        db.session.query(
            Tag.id,
            Tag.name.label("tag_name"),
            func.count(post_x_tag.c.post_id).label("post_count"),
        )
        .join(post_x_tag, Tag.id == post_x_tag.c.tag_id)
        .group_by(Tag.id, Tag.name)
        .order_by(func.count(post_x_tag.c.post_id).desc())
        .limit(15)
        .all()
    )
    return top_tags
