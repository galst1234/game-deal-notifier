import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from commands.subscription.common import NOTIFICATION_NAME_FORMAT
from utils import validate_allowed_chats_async

logger = logging.getLogger(__name__)


@validate_allowed_chats_async
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is not None:
        chat_id = update.effective_chat.id
        job_queue = context.job_queue
        if job_queue is None:
            logger.error("No job_queue found in context")
            await context.bot.send_message(chat_id=chat_id, text="An error occurred, please try again later")
            return

        for job in job_queue.get_jobs_by_name(NOTIFICATION_NAME_FORMAT.format(chat_id=chat_id)):
            job.schedule_removal()

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Successfully unsubscribed")


unsubscribe_handler = CommandHandler("unsubscribe", unsubscribe)
