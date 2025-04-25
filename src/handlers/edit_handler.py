from src.database.connection import connect, disconnect
from src.utils.crypto import encrypt_data, decrypt_data, fernet
from src.utils.helpers import escape_markdown, should_remove_notes
from src.utils.common import is_admin, delete
from src.config import logger


logger = logger.get_logger(__name__)


def register_edit_handlers(bot):
    @bot.message_handler(commands=["edit"])
    async def edit_entry(message):
        if not is_admin(message):
            return await delete(bot, message, await bot.reply_to(message, "⛔ Access denied"))

        try:
            text = message.text[6:].strip()
            service_input, field, new_value = map(str.strip, text.split(" ", 2))
            field = field.lower()
            db_field = "username" if field == "login" else field
        except ValueError:
            help_text = (
                r"🔧 Usage: `/edit <service/ID> <field> <new_value>`"+"\n\n"
                r"📋 Available fields:"+"\n"
                r"• `service` \- Rename service"+"\n"
                r"• `login` \- Change username"+"\n"
                r"• `password` \- Update password"+"\n"
                r"• `notes` \- Edit notes"
            )
            return await delete(bot, message, await bot.reply_to(message, help_text, parse_mode="MarkdownV2"))

        valid_fields = {"service", "login", "password", "notes"}
        if field not in valid_fields:
            return await delete(bot, message, await bot.reply_to(
                message, f"❌ Invalid field '{field}'. Available: service, login, password, notes",
                parse_mode="MarkdownV2"))

        cursor, connection = connect()
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
            current_service_name = decrypt_data(encrypted_service)

            if field == "service":
                cursor.execute("SELECT encrypted_service FROM passwords")
                existing_services = [
                    decrypt_data(e[0]).lower() for e in cursor.fetchall()
                    ]

                if (
                        new_value.lower() in existing_services
                        and new_value.lower() != current_service_name.lower()
                ):
                    return await delete(
                        bot,
                        message,
                        await bot.reply_to(
                            message,
                            f"⚠️ Service `{escape_markdown(new_value)}` already exists",
                            parse_mode="MarkdownV2",
                            ),
                        )
                update_value = encrypt_data(new_value.lower())
            elif field == "password":
                update_value = fernet.encrypt(new_value.encode("utf-8"))
            else:
                if field == "notes" and should_remove_notes(new_value):
                    new_value = ""
                update_value = encrypt_data(new_value)

            cursor.execute(
                f"UPDATE passwords SET encrypted_{db_field} = ? WHERE rowid = ?",
                (update_value, rowid),
                )
            connection.commit()

            display_value = (
                "••••••••" if field == "password" else escape_markdown(new_value)
            )
            success_msg = (
                f"✅ Updated `{escape_markdown(field)}` for `{escape_markdown(current_service_name)}`\n\n"
                f"New value: `{display_value}`"
            )
            await delete(
                bot,
                message,
                await bot.reply_to(message, success_msg, parse_mode="MarkdownV2"),
                )

        except Exception as e:
            logger.error(f"Edit error: {e}")
            await delete(
                bot,
                message,
                await bot.reply_to(
                    message, f"❌ Failed to update: {str(e)}", parse_mode=None
                    ),
                )
        finally:
            if connection:
                disconnect(connection)
