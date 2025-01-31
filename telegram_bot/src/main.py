import logging

from telegram.ext import ApplicationBuilder

from commands import start_handler, unknown_handler
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(start_handler)
    application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
