from telebot import types
from src.database.connection import connect, disconnect
from src.utils.crypto import decrypt_data
from src.utils.helpers import escape_markdown
from src.utils.common import is_admin, delete
from src.config import logger


logger = logger.get_logger(__name__)


def format_service_list(services: list, start: int = 0) -> str:
    if not services:
        return "📭 Empty. Use /add to start"

    chunk = services[start: start + 10]
    total_pages = (len(services) + 9) // 10
    current_page = (start // 10) + 1

    list_text = "🔢 *Your Vault*\n\n" + "\n".join(
        f"▫️ **{rowid}** `{escape_markdown(service)}`"
        for rowid, service in sorted(chunk, key=lambda x: x[0])
    )
    return f"{list_text}\n\n📄 Page *{current_page}* of *{total_pages}*"


async def display_service_page(bot, message, services, page, edit=False):
    start_index = page * 10
    text = format_service_list(services, start_index)

    buttons = []
    if page > 0:
        buttons.append(
            types.InlineKeyboardButton(
                "⬅️ Previous", callback_data=f"list_{page - 1}"
            )
        )
    if start_index + 10 < len(services):
        buttons.append(
            types.InlineKeyboardButton("Next ➡️", callback_data=f"list_{page + 1}")
        )

    markup = types.InlineKeyboardMarkup([buttons]) if buttons else None

    if edit:
        await bot.edit_message_text(
            text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markup,
            parse_mode="MarkdownV2",
        )
    else:
        await delete(
            bot,
            message,
            await bot.reply_to(
                message, text, reply_markup=markup, parse_mode="MarkdownV2"
            ),
        )


def register_list_handlers(bot):
    @bot.message_handler(commands=["list"])
    async def list_services(message):
        if not is_admin(message):
            return await delete(
                bot, message, await bot.reply_to(message, "⛔ Access denied")
            )

        cursor, connection = connect(message.from_user.id)
        try:
            cursor.execute(
                "SELECT rowid, encrypted_service FROM passwords ORDER BY rowid ASC"
            )
            services = [
                (rowid, decrypt_data(encrypted_service))
                for rowid, encrypted_service in cursor.fetchall()
            ]

            if not services:
                return await delete(
                    bot,
                    message,
                    await bot.reply_to(
                        message,
                        r"📭 Empty\. Use /add to start",
                        parse_mode="MarkdownV2",
                    ),
                )

            await display_service_page(bot, message, services, 0)
        except Exception as e:
            logger.error(f"List error: {e}")
            await delete(bot, message, await bot.reply_to(message, "⚠️ Failed to list"))
        finally:
            disconnect(connection)

    @bot.callback_query_handler(func=lambda cb: cb.data.startswith("list_"))
    async def handle_pagination(callback):
        cursor, connection = connect(callback.from_user.id)
        try:
            _, page_str = callback.data.split("_")
            page = int(page_str)

            cursor.execute(
                "SELECT rowid, encrypted_service FROM passwords ORDER BY rowid ASC"
            )
            services = [
                (rowid, decrypt_data(encrypted_service))
                for rowid, encrypted_service in cursor.fetchall()
            ]

            await display_service_page(bot, callback.message, services, page, edit=True)
            await bot.answer_callback_query(callback.id)
        except Exception as e:
            logger.error(f"Pagination error: {e}")
            await bot.answer_callback_query(
                callback.id, "⚠️ Failed to load", show_alert=True
            )
        finally:
            if connection:
                disconnect(connection)
