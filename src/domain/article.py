from pydantic import BaseModel


class Article(BaseModel):
    """
    Representation of a news
    """

    title: str
    description: str
    category: str
    english_translation: str
