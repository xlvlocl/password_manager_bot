from src.config import logger
from src.database.connection import connect, disconnect
from src.utils.common import is_admin, delete
from src.utils.crypto import encrypt_data, fernet
from src.utils.helpers import should_remove_notes, escape_markdown

logger = logger.get_logger(__name__)


def register_add_handlers(bot):
    @bot.message_handler(commands=["add"])
    async def add_service(message):
        if not is_admin(message):
            return await delete(bot, message, await bot.reply_to(message, "⛔ Access denied"))

        try:
            parts = message.text[5:].strip().split(" ", 3)
            if len(parts) < 3:
                raise ValueError

            service, username, password = parts[0].strip().lower(), parts[1].strip(), parts[2].strip()
            notes = parts[3].strip() if len(parts) > 3 and not should_remove_notes(parts[3]) else ""
        except ValueError:
            help_text = (
                r"📝 Usage: `/add <service> <username> <password> \[notes\]`"+"\n\n"
                r"Examples:"+"\n"
                r"`/add amazon user@email\.com Pass123`"+"\n"
                r"`/add google user@gmail\.com pass123 \"Work\"`"
            )
            return await delete(bot, message, await bot.reply_to(message, help_text, parse_mode="MarkdownV2"))

        cursor, connection = None, None
        try:
            cursor, connection = connect(message.from_user.id)

            cursor.execute(
                "SELECT 1 FROM passwords WHERE encrypted_service = ?",
                (encrypt_data(service),),
                )
            if cursor.fetchone():
                return await delete(
                    bot,
                    message,
                    await bot.reply_to(
                        message,
                        f"⚠️ Service `{escape_markdown(service)}` exists\n\n"
                        f"Use `/edit {escape_markdown(service)} login|password|notes new_value`",
                        parse_mode="MarkdownV2",
                        ),
                    )

            cursor.execute(
                "INSERT INTO passwords (encrypted_service, encrypted_username, encrypted_password, encrypted_notes) "
                "VALUES (?, ?, ?, ?)",
                (
                    encrypt_data(service),
                    encrypt_data(username),
                    fernet.encrypt(password.encode("utf-8")),
                    encrypt_data(notes),
                    ),
                )
            connection.commit()

            success_msg = (
                f"✅ *Added successfully\\!*\n\n"
                f"🔐 Service: `{escape_markdown(service)}`\n"
                f"👤 Username: `{escape_markdown(username)}`\n"
                f"🔑 Password: `{'•' * len(password)}`\n"
                f"📝 Notes: `{escape_markdown(notes) if notes else 'None'}`\n\n"
                f"🆔 ID: `{cursor.lastrowid}`"
            )
            await delete(
                bot,
                message,
                await bot.reply_to(message, success_msg, parse_mode="MarkdownV2"),
                )
        except Exception as e:
            logger.error(f"Add error: {e}", exc_info=True)
            await delete(
                bot,
                message,
                await bot.reply_to(
                    message, f"❌ Failed: {str(e)}", parse_mode=None
                    ),
                )
        finally:
            if connection:
                disconnect(connection)
