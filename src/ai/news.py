import os
from loguru import logger

from src.model.article import Article
from src.model.news import News
from src.ai.models.model import AIModelProtocol


class NewsAI:
    """
    Obtain structured data from some news
    """

    model: AIModelProtocol
    news: list[Article]
    batch_size: int
    mock_response: bool

    def __init__(
        self, model: AIModelProtocol, batch_size=10, mock_response=False
    ) -> None:
        """
        Initialize the library with the provided model
        """
        self.model = model
        self.news = []
        self.batch_size = batch_size
        self.mock_response = mock_response

    def _mock_news_response(self) -> None:
        """
        In order to save money during development use an old response to return a mock of the obtained data
        """
        with open(
            os.path.join("src", "ai", "mock", "example.json"), mode="r", encoding="utf8"
        ) as f:
            self.news = News.model_validate_json(f.read()).news

    def classify_news(self, content: str | list[str]) -> None:
        """
        This method will find the news in the provided content and save them inside this class
        """
        system_prompt = """\
        - You are in charge of organizing the news provided by the user.
        - Extract and return a list of news, each defined by a title and a brief description that is not sensationalism but objective.
        - Make a summary translation to english.
        - Assign the news to a category, like for example 'sport', 'german politics', 'international politics', 'tabloid'...
        - Ensure that multiple news items are extracted if available.
        - Make sure you do not miss any translation and that the category is in english.
        - Format the output as a JSON list of News objects.
        """
        if self.mock_response is True:
            self._mock_news_response()
            return

        if isinstance(content, str):
            content = [content]

        for i in range(0, len(content), self.batch_size):
            news_batch = content[i : i + self.batch_size]

            news_text = "\n".join(news_batch)

            response = self.model.generate(
                news_text, system_prompt=system_prompt, response_format=News
            )

            logger.trace(response.content)
            logger.trace(response.metadata)
            logger.trace(response.raw_response)
            logger.trace(type(response.content))
            logger.trace(type(response.metadata))
            logger.trace(type(response.raw_response))

            self.news = self.news + News.model_validate_json(response.content).news

        logger.debug(f"A total of {self.model.used_tokens} tokens were used")
