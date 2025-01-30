import os

ALLOWED_CHATS: list[int] = [int(chat_id) for chat_id in os.getenv("ALLOWED_CHATS").split(",")]
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
