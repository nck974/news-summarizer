# News summarizer

This small tool reads the content of a set of news papers, and organizes it to then send it summarized skipping the configured content.

## Installation

1. Create a virtual environment and install the dependencies:

    ```python
    python -m virtualenv .venv
    .\.venv\Scripts\activate
    pip install poetry
    poetry install
    playwright install
    ```

2. Create a `.env` file with your openapi key following the format of the file [`example.env`](example.env).

## Usage

1. Run `python main.py`

## Roadmap

- [ X ] Extract plain text news from a page.
- [ X ] Extract structured news from the text content with AI.
- [ X ] Classify the structured news into relevant topics.
- [ ] Filter the topics that are not interesting.
- [ ] Send the news via telegram bots.
- [ ] Pack the content in docker.
- [ ] Store in a database the news.
- [ ] Store statistics per day of the different news types.
