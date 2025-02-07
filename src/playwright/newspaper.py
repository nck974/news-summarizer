from typing import Callable
from playwright.sync_api import sync_playwright, Playwright, Browser, Page


class NewspaperContentGatherer:
    """
    Class to interact with the frontend
    """

    playwright: Playwright
    browser: Browser
    page: Page

    def __init__(self, headed=False):
        """
        Initialize the browser
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headed is False)
        self.page = self.browser.new_page()

    def access_page(self, url: str) -> None:
        """
        Access the provided site
        """
        self.page.goto(url)

    def save_screenshot(self) -> None:
        """
        Access the provided site
        """
        self.page.screenshot(path="test.png", type="png")

    def extract_text_content(self) -> str:
        """
        Return the whole text of the page
        """
        return self.page.inner_text("//*")

    def execute_custom_function(self, function: Callable) -> None:
        """
        Execute the provided function providing the page as argument
        """
        function(self.page)

    def close(self) -> None:
        """
        Close the object
        """
        self.browser.close()
        self.playwright.stop()
