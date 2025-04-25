from src.database.connection import connect, disconnect
from src.utils.crypto import decrypt_data
from src.utils.helpers import escape_markdown
from src.utils.common import is_admin, delete
from src.config import logger

logger = logger.get_logger(__name__)


def register_delete_handlers(bot):
    @bot.message_handler(commands=["delete"])
    async def delete_service(message):
        if not is_admin(message):
            return await delete(bot, message, await bot.reply_to(message, "⛔ Access denied"))

        service_input = message.text[8:].strip()
        if not service_input:
            help_text = (
                r"🗑️ Usage: `/delete <service/ID>`"+"\n\n"
                r"Examples:"+"\n"
                r"• `/delete amazon`"+"\n"
                r"• `/delete 42`"
            )
            return await delete(bot, message, await bot.reply_to(message, help_text, parse_mode="MarkdownV2"))

        cursor, connection = connect(message.from_user.id)
        try:
            if service_input.isdigit():
                cursor.execute(
                    "SELECT rowid, encrypted_service FROM passwords WHERE rowid = ?",
                    (int(service_input),),
                    )
                result = cursor.fetchone()
            else:
                cursor.execute("SELECT rowid, encrypted_service FROM passwords")
                services = cursor.fetchall()
                result = None

                for rowid, encrypted_service in services:
                    if (
                            decrypt_data(encrypted_service).lower()
                            == service_input.lower()
                    ):
                        result = (rowid, encrypted_service)
                        break

            if not result:
                return await delete(
                    bot,
                    message,
                    await bot.reply_to(
                        message,
                        f"🔍 Service `{escape_markdown(service_input)}` not found",
                        parse_mode="MarkdownV2",
                        ),
                    )

            rowid, encrypted_service = result
            service_name = decrypt_data(encrypted_service)

            cursor.execute("DELETE FROM passwords WHERE rowid = ?", (rowid,))
            connection.commit()

            await delete(
                bot,
                message,
                await bot.reply_to(
                    message,
                    f"✅ Successfully deleted `{escape_markdown(service_name)}`",
                    parse_mode="MarkdownV2",
                    ),
                )
        except Exception as e:
            logger.error(f"Delete error: {e}")
            await delete(
                bot,
                message,
                await bot.reply_to(
                    message, f"❌ Failed to delete: {str(e)}", parse_mode=None
                    ),
                )
        finally:
            if connection:
                disconnect(connection)
