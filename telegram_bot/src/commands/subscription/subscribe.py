import datetime
import logging

import pytz
from telegram import LinkPreviewOptions, Update
from telegram.ext import CallbackContext, CommandHandler, ContextTypes

from commands.subscription.common import NOTIFICATION_NAME_FORMAT
from config import TIMEZONE
from isthereanydeal.giveaways import get_current_giveaways
from isthereanydeal.utils import format_deals_list
from utils import validate_allowed_chats_async
from utils.get_next_time import get_next_time

NOTIFICATION_TIME = datetime.time(9, 0, tzinfo=pytz.timezone(TIMEZONE))
DAILY_INTERVAL = datetime.timedelta(minutes=1)

logger = logging.getLogger(__name__)


@validate_allowed_chats_async
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is not None:
        chat_id = update.effective_chat.id
        job_queue = context.job_queue
        if job_queue is None:
            logger.error("No job_queue found in context")
            await context.bot.send_message(chat_id=chat_id, text="An error occurred, please try again later")
            return

        job_queue.run_repeating(
            callback=_send_notification,
            interval=DAILY_INTERVAL,
            chat_id=chat_id,
            first=get_next_time(NOTIFICATION_TIME),
            name=NOTIFICATION_NAME_FORMAT.format(chat_id=chat_id),
        )
        await context.bot.send_message(chat_id=chat_id, text="Subscribed to daily notifications successfully")


async def _send_notification(context: CallbackContext) -> None:
    job = context.job
    if job is None:
        logger.error("No job found in context")
        return
    if job.chat_id is None:
        logger.error("No chat_id found in job")
        return

    giveaways = get_current_giveaways()
    message = format_deals_list(giveaways, "Current giveaways:")
    if message:
        await context.bot.send_message(
            chat_id=job.chat_id,
            text=message,
            parse_mode="Markdown",
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )


subscribe_handler = CommandHandler("subscribe", subscribe)
