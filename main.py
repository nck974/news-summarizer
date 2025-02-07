"""
Main module to execute this project
"""

from src.playwright.custom.nord_bayern import accept_nord_bayern_cookies
from src.playwright.newspaper import NewspaperContentGatherer

HEADED = True
NEWSPAPERS = {
    "https://www.nordbayern.de/": accept_nord_bayern_cookies,
}


def main():
    """
    Execute main functionality of this project
    """

    newspaper = NewspaperContentGatherer(headed=HEADED)
    for url, custom_function in NEWSPAPERS.items():
        newspaper.access_page(url)

        if custom_function is not None:
            newspaper.execute_custom_function(custom_function)

        text = newspaper.extract_text_content()
        print(text)

    print("Finished")


if __name__ == "__main__":
    main()
