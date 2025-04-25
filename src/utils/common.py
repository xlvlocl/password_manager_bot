import asyncio
from src.config.settings import ADMIN_IDS
from src.config import logger

logger = logger.get_logger(__name__)


async def delete(bot, message, msg, timer=60):
    await asyncio.sleep(timer)
    try:
        await bot.delete_message(message.chat.id, msg.id)
        await bot.delete_message(message.chat.id, message.id)
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")


def is_admin(message):
    return message.from_user.id in ADMIN_IDS
