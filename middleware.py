import logging
from aiogram import BaseMiddleware
from aiogram.types import Message
from logger import logger


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("bot_logs.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger.addHandler(file_handler)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        user = event.from_user
        username = user.username if user.username else "без username"
        event_text = repr(event.text)
        event_type = event.__class__.__name__ 

        logger.info(f"[{event_type}] User {user.id} ({username}): {event_text}")

        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"Ошибка при обработке {event_type} от {user.id}: {e}", exc_info=True)
            await event.answer("❌ Произошла ошибка. Попробуйте позже.")
