from .base import BaseModelWithConfig


class Newspaper(BaseModelWithConfig):
    """
    Representation of a single newspaper
    """

    id: int | None = None
    name: str
    url: str
