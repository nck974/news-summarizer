from pydantic import BaseModel

from model.article import Article


class News(BaseModel):
    """
    Representation of a news
    """

    news: list[Article]
