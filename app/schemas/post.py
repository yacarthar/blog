from typing import Union

from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: str
    author: str
    summary: Union[str, None] = None
    date_created: Union[str, None] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class PostUpdate(BaseModel):
    title: Union[str, None] = None
    author: Union[str, None] = None
    summary: Union[str, None] = None
    date_created: Union[str, None] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")
