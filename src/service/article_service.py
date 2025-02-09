from loguru import logger
from src.db.model.news import News
from src.model.article import Article
from src.db.repository.news_repository import NewsRepository
from src.db.database import Database


class ArticleService:

    article_repository: NewsRepository

    def __init__(self, db: Database):
        self.db = db
        self.article_repository = NewsRepository(db)

    def save_article(
        self, article: Article, category_id: int, newspaper_id: int
    ) -> int:
        logger.debug(f"Saving article '{article.title}' in the database...")

        news = self.article_repository.create(
            News(
                newspaper_id=newspaper_id,
                category_id=category_id,
                article=article.title,
                description=article.description,
                translation=article.english_translation,
            )
        )

        if news.id is None:
            raise RuntimeError("The article could not be saved")

        return news.id

    def exists_article(self, article_title: str) -> bool:
        """
        Find the article in the database
        """
        news = self.article_repository.get_by_name(article_title)
        if news is None:
            return False

        return True
