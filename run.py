import asyncio
from src.bot import bot_instance
from src.config import logger

logger = logger.get_logger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting password manager bot...")
        bot = bot_instance.run()
        asyncio.run(bot.infinity_polling())
    except Exception as e:
        logger.critical(f"Bot crashed: {e}")
