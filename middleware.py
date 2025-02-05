import logging
from aiogram import BaseMiddleware
from aiogram.types import Message

logging.basicConfig(level=logging.INFO, filename="bot_logs.log", 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        user = event.from_user
        logging.info(f"User {user.id} ({user.username}): {event.text}")
        try:
            return await handler(event, data)
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            await event.answer("❌ Произошла ошибка. Попробуйте позже.")