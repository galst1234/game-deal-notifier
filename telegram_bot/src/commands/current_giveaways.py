from telegram import LinkPreviewOptions, Update
from telegram.ext import CommandHandler, ContextTypes

from isthereanydeal.giveaways import get_current_giveaways
from utils import validate_allowed_chats_async


@validate_allowed_chats_async
async def current_giveaways(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is not None:
        giveaways = get_current_giveaways()
        if giveaways:
            message = "Current giveaways:\n"
            for deal in giveaways:
                message += f"- [{deal.title}]({deal.deal.url})\n"
        else:
            message = "No giveaways found."

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode="Markdown",
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )


current_giveaways_handler = CommandHandler("current_giveaways", current_giveaways)
