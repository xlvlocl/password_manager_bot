from src.utils.common import is_admin, delete


def register_start_handlers(bot):
    @bot.message_handler(commands=["start"])
    async def greeting(message):
        if not is_admin(message):
            return await delete(
                bot, message, await bot.reply_to(message, "⛔ Access denied")
            )

        welcome_message = (
            r"🔐 *Password Manager Bot*" + "\n\n"
            r"✨ *Available commands*:" + "\n"
            r"`/start` \- Show this help" + "\n"
            r"`/list` \- List services" + "\n"
            r"`/add <service> <login> <password> \[notes\]`" + "\n"
            r"`/edit <service/ID> <field> <new_value>`" + "\n"
            r"`/delete <service/ID>`" + "\n"
            r"`/password <length>`" + "\n\n"
            r"🔍 *Search*: Type a service name"
        )

        await bot.reply_to(message, welcome_message, parse_mode="MarkdownV2")
