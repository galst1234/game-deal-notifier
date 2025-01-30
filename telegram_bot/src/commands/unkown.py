from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from decorators import validate_allowed_chats_async


@validate_allowed_chats_async
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Command not recognized.")


unknown_handler = MessageHandler(filters.COMMAND, unknown)
