import os
from loguru import logger
from src.db.entity.news import News
from src.domain.article import Article
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

    def _get_max_number_of_news_per_newspaper(self) -> int:
        """
        Return the api key from the environment variable
        """
        articles_number = os.environ.get("MAX_NEWS_PER_NEWSPAPER")
        if articles_number is None:
            return 15
        return int(articles_number)

    def filter_article_limit(self, articles: list[str]) -> list[str]:
        """
        Limit the number of articles found to the configured number
        """
        number = self._get_max_number_of_news_per_newspaper()

        if len(articles) > number:
            return articles[:number]

        return articles
