import secrets
from src.utils.common import is_admin, delete


def register_password_handlers(bot):
    @bot.message_handler(commands=["password"])
    async def generate_password(message):
        if not is_admin(message):
            return await delete(bot, message, await bot.reply_to(message, "⛔ Access denied"))

        try:
            length = int(message.text[9:].strip())
            if length < 8:
                return await delete(
                    bot, message, await bot.reply_to(
                        message, "🔢 Minimum 8 characters", parse_mode="MarkdownV2"
                        )
                    )
            if length > 64:
                return await delete(
                    bot, message, await bot.reply_to(
                        message, "⚠️ Maximum 64 characters", parse_mode="MarkdownV2"
                        )
                    )
        except ValueError:
            help_text = r"📝 Usage: `/password <length>`" + "\n" + r"Example: `/password 12`"
            return await delete(bot, message, await bot.reply_to(message, help_text, parse_mode="MarkdownV2"))

        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+-=?@^_"
        password = "".join(secrets.choice(chars) for _ in range(length))
        escaped_password = "".join(rf"\{c}" for c in password)

        await delete(
            bot, message, await bot.reply_to(
                message,
                fr"🔐 *{length}\-character password:*" + f"\n\n`{escaped_password}`",
                parse_mode="MarkdownV2"
                )
            )
