from datetime import datetime
from pydantic import Field
from .base import BaseModelWithConfig


class News(BaseModelWithConfig):
    """
    Representation of the news
    """

    id: int | None = None
    newspaper_id: int
    category_id: int
    article: str
    description: str | None = None
    translation: str | None = None
    created_at: datetime | None = Field(default_factory=datetime.now)
