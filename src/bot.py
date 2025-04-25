from telebot.async_telebot import AsyncTeleBot
from src.config.settings import BOT_TOKEN
from src.config.logger import get_logger

logger = get_logger(__name__)


class Bot:
    def __init__(self):
        self.bot = AsyncTeleBot(token=BOT_TOKEN)
        self._register_all_handlers()

    def _register_all_handlers(self):
        from src.handlers.start_handler import register_start_handlers
        from src.handlers.add_handler import register_add_handlers
        from src.handlers.list_handler import register_list_handlers
        from src.handlers.edit_handler import register_edit_handlers
        from src.handlers.delete_handler import register_delete_handlers
        from src.handlers.password_handler import register_password_handlers
        from src.handlers.search_handler import register_search_handlers

        register_start_handlers(self.bot)
        register_add_handlers(self.bot)
        register_list_handlers(self.bot)
        register_edit_handlers(self.bot)
        register_delete_handlers(self.bot)
        register_password_handlers(self.bot)
        register_search_handlers(self.bot)

    def run(self):
        logger.info("Bot started")
        return self.bot


bot_instance = Bot()
