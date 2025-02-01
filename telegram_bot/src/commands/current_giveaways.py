from telegram import LinkPreviewOptions, Update
from telegram.ext import CommandHandler, ContextTypes

from isthereanydeal.deals_list import DealItem, IsThereAnyDealDealsList, build_deals_url
from utils import validate_allowed_chats_async
from utils.pagination import follow_pagination


@validate_allowed_chats_async
async def current_giveaways(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is not None:
        deals: list[DealItem] = follow_pagination(
            initial_url=build_deals_url(),
            paginated_result_class=IsThereAnyDealDealsList,
            should_continue=lambda result: result.items[-1].deal.price.amount == 0,
            is_valid=lambda item: item.deal.price.amount == 0,
        )
        if deals:
            message = "Current giveaways:\n"
            for deal in deals:
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
