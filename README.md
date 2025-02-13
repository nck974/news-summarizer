# News summarizer

This small tool reads the content of a set of news papers, and classifies the news into categories. Then sends the news through Telegram.

Implemented newspapers:

☑ 20minutos.es
☑ nordbayern.de

## Installation

### Local

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

### Docker

1. Pull the project
1. Build `docker compose build`.
1. Configure the `.env` file.
1. Start `docker compose up -d`.

## Usage

1. Run `python main.py`

## Configuration

| Property | Description | Type | Required |
|----------|-------------|------|----------|
| OPENAI_API_KEY | Authentication key for accessing the OpenAI API services. Obtain this from your OpenAI account dashboard. | String | Yes |
| TELEGRAM_BOT_API_KEY | Authentication token for your Telegram bot. Get this from BotFather when creating a new bot. | String | Yes |
| TELEGRAM_USER_CHAT_ID | Unique identifier for the Telegram chat where messages will be sent. Can be obtained by sending a message to your bot and checking the chat ID. | String | Yes |
| FILTER_CATEGORIES | List of categories to filter content. Multiple categories should be comma-separated. | String | No |
| CRON_PATTERN | Schedule pattern in cron format (e.g., "0 8 ** *"). Defines when the tasks will run. | String | Yes |
