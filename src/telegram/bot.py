import os
import telebot
from dotenv import load_dotenv


class TelegramBot:
    """
    Bot that takes care of sending the messages through telegram
    """

    bot: telebot.TeleBot

    def __init__(self) -> None:
        """
        Initialize the bot
        """
        api_key = os.environ.get("TELEGRAM_BOT_API_KEY")
        if api_key is None:
            raise RuntimeError(
                "TELEGRAM_BOT_API_KEY environment variable is not defined"
            )

        self.bot = telebot.TeleBot(api_key)

    def _get_chat_ids(self) -> list[str]:
        """
        Obtain the chat ids configured in the environment
        """

        chat_ids = os.environ.get("TELEGRAM_USER_CHAT_ID")
        if chat_ids is None:
            raise RuntimeError(
                "TELEGRAM_USER_CHAT_ID environment variable is not defined"
            )
        return [x.strip() for x in chat_ids.split(",")]

    def _chunk_message(self, message: str, chunk_size=4096) -> list[str]:
        """
        Divide the message if it is too long. As telegram is limited to 4096.
        See: https://limits.tginfo.me/en
        """
        return [message[i : i + chunk_size] for i in range(0, len(message), chunk_size)]

    def broadcast_message(self, message: str) -> None:
        """
        Broadcast a message
        """
        for chat_id in self._get_chat_ids():
            for message_chunk in self._chunk_message(message):
                self.bot.send_message(chat_id, message_chunk, parse_mode="MARKDOWN")


if __name__ == "__main__":
    # Use this library directly to verify that the communication with your chat works as expected
    load_dotenv()
    bot = TelegramBot()
    bot.broadcast_message("Hello everyone!")
