from pydantic import BaseModel

from src.model.article import Article


class News(BaseModel):
    """
    Representation of a news
    """

    news: list[Article]
