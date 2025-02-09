from typing import Any, Callable
from playwright.sync_api import sync_playwright, Playwright, Browser, Page


class NewspaperContentGatherer:
    """
    Class to interact with the frontend
    """

    playwright: Playwright
    browser: Browser
    page: Page
    mock_extract_news: bool

    def __init__(self, headed=False, mock_extract_news=False):
        """
        Initialize the browser
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headed is False)
        self.page = self.browser.new_page()
        self.mock_extract_news = mock_extract_news

    def access_page(self, url: str) -> None:
        """
        Access the provided site
        """
        if self.mock_extract_news:
            return

        self.page.goto(url)

    def save_screenshot(self) -> None:
        """
        Access the provided site
        """
        self.page.screenshot(path="test.png", type="png")

    def extract_root_text_content(self) -> list[str]:
        """
        Return the whole text of the page
        """
        if self.mock_extract_news:
            return ["SOME_TEXT"]

        return [self.page.inner_text("//*")]

    def execute_custom_function(self, function: Callable) -> None:
        """
        Execute the provided function providing the page as argument
        """
        if self.mock_extract_news:
            return

        function(self.page)

    def execute_custom_function_returning_value(self, function: Callable) -> Any:
        """
        Execute the provided function providing the page as argument
        """
        if self.mock_extract_news:
            return ["SOME_TEXT"]

        return function(self.page)

    def close(self) -> None:
        """
        Close the object
        """
        self.browser.close()
        self.playwright.stop()
