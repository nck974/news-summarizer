from .base import BaseModelWithConfig


class Category(BaseModelWithConfig):
    """
    Representation of a category
    """

    id: int | None = None
    name: str
