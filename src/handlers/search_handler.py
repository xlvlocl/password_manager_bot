from src.database.connection import connect, disconnect
from src.utils.crypto import decrypt_data, fernet
from src.utils.helpers import escape_markdown
from src.utils.common import is_admin, delete
from src.config import logger


logger = logger.get_logger(__name__)


def register_search_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    async def get_password(message):
        if not is_admin(message):
            return await delete(bot, message, await bot.reply_to(message, "⛔ Access denied"))

        search_input = message.text.strip().lower()
        if not search_input:
            return await delete(bot, message, await bot.reply_to(
                message, "🔍 Please enter a service name or ID", parse_mode="MarkdownV2"))

        cursor, connection = connect()
        try:
            if search_input.isdigit():
                cursor.execute(
                    "SELECT encrypted_service, encrypted_username, encrypted_password, encrypted_notes "
                    "FROM passwords WHERE rowid = ?",
                    (int(search_input),),
                    )
                row = cursor.fetchone()
            else:
                cursor.execute(
                    "SELECT rowid, encrypted_service, encrypted_username, encrypted_password, encrypted_notes FROM passwords"
                    )
                rows = cursor.fetchall()
                row = None

                for db_row in rows:
                    decrypted_name = decrypt_data(db_row[1])
                    decrypted_user = decrypt_data(db_row[2])

                    if (
                            decrypted_name.lower() == search_input.lower()
                            or decrypted_user.lower() == search_input.lower()
                    ):
                        row = db_row[1:]
                        break

            if not row:
                return await delete(
                    bot,
                    message,
                    await bot.reply_to(
                        message,
                        f"🔍 No service found matching `{escape_markdown(search_input)}`",
                        parse_mode="MarkdownV2",
                        ),
                    )

            service = decrypt_data(row[0])
            username = decrypt_data(row[1])
            password = "".join(
                rf"\{c}" for c in fernet.decrypt(row[2]).decode("utf-8")
                )
            notes = decrypt_data(row[3]) if row[3] else " "

            response = (
                f"🔍 Found:\n\n"
                f"🔐 *Service:* `{escape_markdown(service)}`\n"
                f"👤 *Username:* `{escape_markdown(username)}`\n"
                f"🔑 *Password:* `{password}`\n"
                f"📝 *Notes:* `{escape_markdown(notes)}`"
            )
            await delete(
                bot,
                message,
                await bot.reply_to(message, response, parse_mode="MarkdownV2"),
                )

        except Exception as e:
            logger.error(f"Search error: {e}")
            await delete(
                bot,
                message,
                await bot.reply_to(
                    message, f"❌ Search failed: {str(e)}", parse_mode=None
                    ),
                )
        finally:
            if connection:
                disconnect(connection)
