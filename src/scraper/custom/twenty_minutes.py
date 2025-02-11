from playwright.sync_api import Page


def extract_20_minutes_headlines(page: Page) -> list[str] | None:
    """
    Close the cookies of the page to be able to read the content
    """
    elements = page.query_selector_all("xpath=//h1/a[contains(@href, '20minutos')]")

    if elements is None:
        return None

    data = []
    for element in elements:
        data.append(element.inner_text())

    return data
