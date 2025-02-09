from pydantic import BaseModel

from src.model.article import Article


class ExtractedNews(BaseModel):
    """
    Representation of a news
    """

    news: list[Article]
