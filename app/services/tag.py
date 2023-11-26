from typing import Union
from app.models import Tag


def get_tag_by_name(tag_name) -> Union[Tag, None]:
    return Tag.find_by_name(tag_name)