import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from config import ALLOWED_CHATS

logger = logging.getLogger(__name__)


# Potentially replace this with an automatic thing that happens on `Application.add_handler`
def validate_allowed_chats_async(
        func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Any],
) -> Callable[[Update, ContextTypes.DEFAULT_TYPE], Any]:
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None:
            return await func(update, context)

        chat_id: int = update.effective_chat.id
        # Temporary solution, this should be replaced with a proper DB
        if chat_id in ALLOWED_CHATS:
            return await func(update, context)
        else:
            logger.info(f"Unauthorized chat id: {chat_id}")
            # Ideally, I want to implement an option to request access, that will send me a message allowing me to
            # approve or deny access, updating the DB accordingly
            await context.bot.send_message(
                chat_id=chat_id,
                text="Sorry but you are currently an unrecognized user. To gain access to the bot please ask the "
                     f"owner to add you to the allowed users. Your chat id: {chat_id}",
            )

    return wrapper
