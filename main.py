"""
Main module to execute this project
"""

import os
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger

from src.ai.models.model import AIModelProtocol
from src.ai.models.openai import OpenAIModel
from src.ai.news import NewsAI
from src.model.news import Article, News
from src.model.newspaper_config import NewspaperConfig
from src.playwright.custom.nord_bayern import (
    accept_nord_bayern_cookies,
    extract_nord_bayern_headlines,
)
from src.playwright.newspaper import NewspaperContentGatherer
from src.telegram.bot import TelegramBot

HEADED = True
BATCH_SIZE = 10
MOCK_AI_RESPONSE = False
MOCK_EXTRACT_NEWS = False
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
) -> str | list[str] | None:
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

    logger.debug(f"A total of {len(news_ai.news)} were found.")
    logger.info("AI analysis finished.")

    return news_ai.news


def save_data(news: list[Article]) -> None:
    """
    Save the data for later usage
    """
    with open("example.json", mode="w", encoding="utf8") as f:
        f.write(News(news=news).model_dump_json(indent=4))


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
        category_message = f"""### {category}\n\n"""
        for index, article in enumerate(
            sorted(
                filter(lambda x: x.category == category, news), key=lambda x: x.title
            ),
            start=1,
        ):
            category_message += (
                f"{index}. *{article.title}*\n"
                f"- *Description:* {article.description}\n"
                f"- *English Translation:* {article.english_translation}\n\n"
            )

        bot.broadcast_message(category_message)


def main():
    """
    Execute main functionality of this project
    """
    model = OpenAIModel(api_key=os.environ.get("OPENAI_API_KEY", ""))
    newspaper_gatherer = NewspaperContentGatherer(
        headed=HEADED, mock_extract_news=MOCK_EXTRACT_NEWS
    )
    bot = TelegramBot()

    for newspaper in NEWSPAPERS:

        text = extract_news(newspaper_gatherer, newspaper)

        if text is None:
            continue

        news = classify_news(model, text)

        if news is None:
            logger.info("No news found on the ai analysis")
            continue

        save_data(news)
        # display_news(news)
        broadcast_news(bot, newspaper.name, news)

    newspaper_gatherer.close()
    print("Finished")


if __name__ == "__main__":
    load_dotenv()
    main()
