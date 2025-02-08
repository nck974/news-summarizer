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


def extract_nord_bayern_headlines(page: Page) -> list[str] | None:
    """
    Close the cookies of the page to be able to read the content
    """
    elements = page.query_selector_all(
        "xpath=//*[(self::h6 or self::h2) and contains(@class, 'headline')] | //h5[contains(@class,'headline') and not(following-sibling::p[text()='anzeige'] or preceding-sibling::p[contains(text(),'Anzeige')])]"
    )

    if elements is None:
        return None

    data = []
    for element in elements:
        data.append(element.inner_text())

    return data
