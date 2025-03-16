from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Entity(BaseModel):
    """
    All files in a folder with the same file name are considered attributes of the same entity.
    """

    name: str
