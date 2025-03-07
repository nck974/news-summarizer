"""
Main module to execute this project
"""

import os

from dotenv import load_dotenv
from loguru import logger

from src.ai.provider.base import AIModelProtocol
from src.ai.provider.openai import OpenAIModel
from src.db.database import Database
from src.domain.news import Article
from src.domain.newspaper import Newspaper
from src.scraper.custom.nord_bayern import (
    accept_nord_bayern_cookies,
    extract_nord_bayern_headlines,
)
from src.scraper.custom.twenty_minutes import (
    extract_20_minutes_headlines,
)
from src.services.ai_service import AiService
from src.services.article_service import ArticleService
from src.services.broadcast_service import BroadcastService
from src.services.category_service import CategoryService
from src.services.newspaper_service import NewspaperService
from src.services.scraper_service import ScraperService
from src.telegram.bot import TelegramBot

HEADED_BROWSER = False
BATCH_SIZE = 10
# Skip the data extraction from the frontend
MOCK_EXTRACT_NEWS = False
# Return a mocked object of the AI instead of wasting credit
MOCK_AI_RESPONSE = False
# Just print in the console the messages that will be broadcasted
DRY_RUN_BROADCAST_MESSAGES = False
# Name of the sqlite file where the database will be saved
DATABASE_NAME = os.path.join("database", "news.db")
NEWSPAPERS = [
    Newspaper(
        name="Nord Bayern",
        url="https://www.nordbayern.de/",
        access_hook=accept_nord_bayern_cookies,
        extract_data_hook=extract_nord_bayern_headlines,
    ),
    Newspaper(
        name="20 Minutos",
        url="https://20minutos.es/",
        access_hook=None,
        extract_data_hook=extract_20_minutes_headlines,
    ),
]


def extract_news(newspaper: Newspaper) -> list[str] | None:
    """
    Extract the news from the newspaper website
    """
    scraper_service = ScraperService(
        headed=HEADED_BROWSER, mock_extract_news=MOCK_EXTRACT_NEWS
    )
    logger.info(f"Extracting data from: {newspaper.name}")

    scraper_service.access_page(newspaper.url)

    if newspaper.access_hook is not None:
        scraper_service.execute_custom_function(newspaper.access_hook)

    text = scraper_service.execute_custom_function_returning_value(
        newspaper.extract_data_hook
    )

    scraper_service.close()

    if text is None or text == "" or (isinstance(text, list) and len(text) == 0):
        return None

    logger.debug(f"News found in {newspaper.url}:\n{text}")

    return text


def classify_news(model: AIModelProtocol, text: list[str] | str) -> list[Article]:
    """
    Use AI to classify the news
    """
    logger.info("Starting AI analysis on the extracted text...")

    news_ai = AiService(model, batch_size=BATCH_SIZE, mock_response=MOCK_AI_RESPONSE)
    news_ai.classify_news(text)
    news_ai.filter_news_by_category()

    logger.debug(f"A total of {len(news_ai.news)} were found.")
    logger.info("AI analysis finished.")

    return news_ai.news


def save_data_in_db(db: Database, newspaper: Newspaper, news: list[Article]) -> None:
    """
    Save the data in the database so that further request can filter the news that have
    already been processed by the AI
    """

    newspaper_service = NewspaperService(db)
    newspaper_id = newspaper_service.save_newspaper(newspaper)

    categories = set([x.category.lower() for x in news])

    category_service = CategoryService(db)
    article_service = ArticleService(db)
    for category in sorted(categories):
        category_id = category_service.save_category(category)
        for article in sorted(
            filter(lambda x: x.category == category, news), key=lambda x: x.title
        ):
            article_service.save_article(article, category_id, newspaper_id)


def filter_existing_news(db: Database, news: list[str]) -> list[str]:
    """
    Filter the news that are already stored in the database
    """
    article_service = ArticleService(db)

    articles: list[str] = []
    for article in news:
        if article_service.exists_article(article):
            continue
        articles.append(article)

    articles = article_service.filter_article_limit(articles)

    logger.debug(f"A total of {len(articles)} new articles were found")

    return articles


def main():
    """
    Execute main functionality of this project
    """
    model = OpenAIModel(api_key=os.environ.get("OPENAI_API_KEY", ""))

    bot = TelegramBot(dry_run=DRY_RUN_BROADCAST_MESSAGES)
    broadcast_service = BroadcastService(bot)
    db = Database(DATABASE_NAME)

    for newspaper in NEWSPAPERS:

        raw_news = extract_news(newspaper)

        if raw_news is None:
            continue

        raw_news = filter_existing_news(db, raw_news)

        news = classify_news(model, raw_news)

        if news is None:
            logger.info("No news found on the ai analysis")
            continue

        save_data_in_db(db, newspaper, news)
        broadcast_service.broadcast_news(newspaper.name, news)

    print("Finished")


if __name__ == "__main__":
    load_dotenv()
    main()
