from telebot import types


def get_list_markup(page, total_pages):
    buttons = []
    if page > 0:
        buttons.append(
            types.InlineKeyboardButton(
                "⬅️ Previous", callback_data=f"list_{page - 1}"
                )
            )
    if page < total_pages - 1:
        buttons.append(
            types.InlineKeyboardButton(
                "Next ➡️", callback_data=f"list_{page + 1}"
                )
            )
    return types.InlineKeyboardMarkup([buttons]) if buttons else None
