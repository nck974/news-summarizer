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

3. Create a telegram bot.
    1. Search in telegram `@BotFather`.
    2. Send command `/newbot`.
    3. Follow de instructions.
    4. Add the HTTP API key to your `.env`.

4. Contact your bot and get a your chat_id.
    1. Contact in telegram `@userinfobot`.
    2. Add your chat id to the `.env` in `TELEGRAM_USER_CHAT_ID`. (Many chat ids can be provided separated by a `,`)

5. Add the categories you want to filter to the `.env` in the property `FILTER_CATEGORIES`, separated by a `,`. You may want to extend this after you see what comes from the AI.

## Usage

1. Run `python main.py`

## Roadmap

- [ X ] Extract plain text news from a page.
- [ X ] Extract structured news from the text content with AI.
- [ X ] Classify the structured news into relevant topics.
- [ X ] Filter the categories that are not interesting.
- [ X ] Send the news via telegram bot.
- [ ] Pack the content in docker.
- [ X ] Store in a database the news.
- [ ] Store statistics per day of the different news types.
