from isthereanydeal.deals_list import DealItem


def format_deals_list(items: list[DealItem], title: str | None = None) -> str | None:
    if not items:
        return None

    message = f"{title}\n" if title else ""
    for deal in items:
        message += f"- [{deal.title}]({deal.deal.url}) on {deal.deal.shop.name}\n"

    return message
