from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from decorators import validate_allowed_chats_async


@validate_allowed_chats_async
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Currently under construction 🏗")


start_handler = CommandHandler("start", start)
