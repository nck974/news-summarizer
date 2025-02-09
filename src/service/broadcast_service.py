from datetime import datetime
from loguru import logger
from model.article import Article
from src.telegram.bot import TelegramBot


class BroadcastService:
    """
    Class in charge of sending the news across the configured channels
    """

    def __init__(self, telegram_bot: TelegramBot):
        self.telegram_bot = telegram_bot

    def broadcast_news(self, newspaper_name: str, news: list[Article]) -> None:
        """
        Displayed the articles that were provided
        """
        logger.info(f"Sending broadcast message with the news of {newspaper_name}...")

        categories = set([x.category for x in news])

        logger.debug(f"The following categories were found: {categories}")

        self.telegram_bot.broadcast_message(
            f"""**News from {newspaper_name} ({datetime.now().strftime(r"%Y-%m-%d")}):**"""
        )
        for category in sorted(categories):
            category_message = f"""### {category.capitalize()}\n\n"""
            for index, article in enumerate(
                sorted(
                    filter(lambda x: x.category == category, news),
                    key=lambda x: x.title,
                ),
                start=1,
            ):
                category_message += (
                    f"{index}. *{article.english_translation}*\n"
                    f"- *Original title:* {article.title}\n"
                    f"- *Description:* {article.description}\n\n"
                )

            self.telegram_bot.broadcast_message(category_message)
