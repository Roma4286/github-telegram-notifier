import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..config import settings

logger = logging.getLogger(__name__)

bot = Bot(token=settings.telegram_bot_token)

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    if message.from_user is None:
        return
    logger.info("/start from user %s", message.from_user.id)
    await message.answer(f"Your id: {message.from_user.id}")


async def send_message(chat_id: int, text: str) -> bool:
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except TelegramAPIError as e:
        logger.warning("Failed to send message to chat %s: %s", chat_id, e)
        return False
    return True


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
