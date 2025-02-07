import time
from playwright.sync_api import Page


def accept_nord_bayern_cookies(page: Page):
    """
    Close the cookies of the page to be able to read the content
    """
    element = page.locator("div#cmpwrapper >> #cmpwelcomebtnyes")

    if element is None:
        print("Cookies not found")
        return

    element.click()
    # Wait till JS is executed
    time.sleep(0.5)
