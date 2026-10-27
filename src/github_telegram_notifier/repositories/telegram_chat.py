from collections.abc import Sequence

from sqlalchemy import select

from ..models import Telegram_chat
from .base import BaseRepository


class TelegramChatRepository(BaseRepository[Telegram_chat]):
    model = Telegram_chat

    async def create(
        self, *, user_id: int, chat_id: int, title: str | None = None
    ) -> Telegram_chat:
        return await self.add(
            Telegram_chat(user_id=user_id, chat_id=chat_id, title=title)
        )

    async def get_by_chat_id(self, chat_id: int) -> Sequence[Telegram_chat]:
        stmt = select(Telegram_chat).where(Telegram_chat.chat_id == chat_id)
        return (await self.session.scalars(stmt)).all()

    async def get_by_user(self, user_id: int) -> Sequence[Telegram_chat]:
        stmt = select(Telegram_chat).where(Telegram_chat.user_id == user_id)
        return (await self.session.scalars(stmt)).all()
