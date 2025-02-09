from pydantic import BaseModel

from src.domain.article import Article


class ExtractedNews(BaseModel):
    """
    Representation of a news
    """

    news: list[Article]
