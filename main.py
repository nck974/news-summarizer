"""
Main module to execute this project
"""

import os
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger

from src.db.model.category import Category
from src.db.model.news import News
from src.db.repository.category_repository import CategoryRepository
from src.db.repository.news_repository import NewsRepository
from src.db.database import Database
from src.db.model.newspaper import Newspaper
from src.db.repository.newspaper_repository import NewspaperRepository
from src.ai.models.model import AIModelProtocol
from src.ai.models.openai import OpenAIModel
from src.ai.news import NewsAI
from src.model.news import Article, ExtractedNews
from src.model.newspaper_config import NewspaperConfig
from src.playwright.custom.nord_bayern import (
    accept_nord_bayern_cookies,
    extract_nord_bayern_headlines,
)
from src.playwright.newspaper import NewspaperContentGatherer
from src.telegram.bot import TelegramBot

HEADED = True
BATCH_SIZE = 10
# Skip the data extraction from the frontend
MOCK_EXTRACT_NEWS = False
# Return a mocked object of the AI instead of wasting credit
MOCK_AI_RESPONSE = True
# Just print in the console the messages that will be broadcasted
DRY_RUN_BROADCAST_MESSAGES = True
# Name of the sqlite file where the database will be saved
DATABASE_NAME = "news.db"
NEWSPAPERS = [
    NewspaperConfig(
        name="Nord Bayern",
        url="https://www.nordbayern.de/",
        access_hook=accept_nord_bayern_cookies,
        extract_data_hook=extract_nord_bayern_headlines,
    )
]


def extract_news(
    newspaper_gatherer: NewspaperContentGatherer, newspaper: NewspaperConfig
) -> list[str] | None:
    """
    Extract the news from the newspaper website
    """

    logger.info(f"Extracting data from: {newspaper.name}")

    newspaper_gatherer.access_page(newspaper.url)

    if newspaper.access_hook is not None:
        newspaper_gatherer.execute_custom_function(newspaper.access_hook)

    if newspaper.extract_data_hook is None:
        text = newspaper_gatherer.extract_root_text_content()
    else:
        text = newspaper_gatherer.execute_custom_function_returning_value(
            newspaper.extract_data_hook
        )

    if text is None or text == "" or (isinstance(text, list) and len(text) == 0):
        return None

    logger.debug(f"Mews found in {newspaper.url}:\n{text}")

    return text


def classify_news(model: AIModelProtocol, text: list[str] | str) -> list[Article]:
    """
    Use AI to classify the news
    """
    logger.info("Starting AI analysis on the extracted text...")

    news_ai = NewsAI(model, batch_size=BATCH_SIZE, mock_response=MOCK_AI_RESPONSE)
    news_ai.classify_news(text)
    news_ai.filter_news()

    logger.debug(f"A total of {len(news_ai.news)} were found.")
    logger.info("AI analysis finished.")

    return news_ai.news


def save_data(db: Database, newspaper: NewspaperConfig, news: list[Article]) -> None:
    """
    Save the data for later usage
    """

    newspaper_id = save_newspaper_in_db(db, newspaper)

    categories = set([x.category.lower() for x in news])

    for category in sorted(categories):
        category_id = save_category_in_db(db, category)
        for article in sorted(
            filter(lambda x: x.category == category, news), key=lambda x: x.title
        ):
            save_article_in_db(db, article, category_id, newspaper_id)

    with open("example.json", mode="w", encoding="utf8") as f:
        f.write(ExtractedNews(news=news).model_dump_json(indent=4))


def filter_existing_news(db: Database, news: list[str]) -> list[str]:
    """
    Save the data for later usage
    """

    articles: list[str] = []
    for article in news:
        if exists_article_in_db(db, article):
            continue
        articles.append(article)

    return articles


def display_news(news: list[Article]) -> None:
    """
    Displayed the articles that were provided
    """
    for index, article in enumerate(news):
        print(
            f"{index} ({article.category}): {article.title}\n\t`--> {article.description}\n\t`--> {article.english_translation}"
        )


def broadcast_news(bot: TelegramBot, newspaper_name: str, news: list[Article]) -> None:
    """
    Displayed the articles that were provided
    """
    logger.info(f"Sending broadcast message with the news of {newspaper_name}...")

    categories = set([x.category for x in news])

    logger.debug(f"The following categories were found: {categories}")

    bot.broadcast_message(
        f"""**News from {newspaper_name} ({datetime.now().strftime(r"%Y-%m-%d")}):**"""
    )
    for category in sorted(categories):
        category_message = f"""### {category.capitalize()}\n\n"""
        for index, article in enumerate(
            sorted(
                filter(lambda x: x.category == category, news), key=lambda x: x.title
            ),
            start=1,
        ):
            category_message += (
                f"{index}. *{article.english_translation}*\n"
                f"- *Original title:* {article.title}\n"
                f"- *Description:* {article.description}\n\n"
            )

        bot.broadcast_message(category_message)


def save_newspaper_in_db(db: Database, newspaper_config: NewspaperConfig) -> int:
    """
    Save the newspaper in the database if it does not already exist
    """
    logger.debug(f"Saving newspaper '{newspaper_config.name}' in the database...")
    newspaper_repo = NewspaperRepository(db)
    newspaper = newspaper_repo.get_by_name(newspaper_config.name)
    if newspaper is None:
        newspaper = newspaper_repo.create(
            Newspaper(name=newspaper_config.name, url=newspaper_config.url)
        )

    if newspaper.id is None:
        raise RuntimeError("The newspaper could not be saved")

    return newspaper.id


def exists_article_in_db(db: Database, article_title: str) -> bool:
    """
    Find the article in the database
    """
    news_repo = NewsRepository(db)
    news = news_repo.get_by_name(article_title)
    if news is None:
        return False

    return True


def save_category_in_db(db: Database, category_name: str) -> int:
    """
    Save the category in the database if it does not already exist
    """
    logger.debug(f"Saving category '{category_name}' in the database...")
    category_repo = CategoryRepository(db)
    category = category_repo.get_by_name(category_name)
    if category is None:
        category = category_repo.create(Category(name=category_name))

    if category.id is None:
        raise RuntimeError("The category could not be saved")

    return category.id


def save_article_in_db(
    db: Database, article: Article, category_id: int, newspaper_id: int
) -> int:
    """
    Save the category in the database if it does not already exist
    """
    logger.debug(f"Saving article '{article.title}' in the database...")
    news_repo = NewsRepository(db)
    news = news_repo.create(
        News(
            newspaper_id=newspaper_id,
            category_id=category_id,
            article=article.title,
            description=article.description,
            translation=article.english_translation
        )
    )

    if news.id is None:
        raise RuntimeError("The article could not be saved")

    return news.id


def main():
    """
    Execute main functionality of this project
    """
    model = OpenAIModel(api_key=os.environ.get("OPENAI_API_KEY", ""))
    newspaper_gatherer = NewspaperContentGatherer(
        headed=HEADED, mock_extract_news=MOCK_EXTRACT_NEWS
    )
    bot = TelegramBot(dry_run=DRY_RUN_BROADCAST_MESSAGES)
    db = Database(DATABASE_NAME)

    for newspaper in NEWSPAPERS:

        raw_news = extract_news(newspaper_gatherer, newspaper)

        if raw_news is None:
            continue

        raw_news = filter_existing_news(db, raw_news)

        news = classify_news(model, raw_news)

        if news is None:
            logger.info("No news found on the ai analysis")
            continue

        save_data(db, newspaper, news)
        # display_news(news)
        broadcast_news(bot, newspaper.name, news)

    newspaper_gatherer.close()
    print("Finished")


if __name__ == "__main__":
    load_dotenv()
    main()
