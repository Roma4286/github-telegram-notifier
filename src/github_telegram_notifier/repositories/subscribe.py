from collections.abc import Sequence

from sqlalchemy import select

from ..models import Subscribe
from .base import BaseRepository


class SubscribeRepository(BaseRepository[Subscribe]):
    model = Subscribe

    async def create(
        self, *, telegram_chat_id: int, github_repository_id: int, title: str
    ) -> Subscribe:
        return await self.add(
            Subscribe(
                telegram_chat_id=telegram_chat_id,
                github_repository_id=github_repository_id,
                title=title,
            )
        )

    async def get_by_ids(
        self, *, telegram_chat_id: int, github_repository_id: int
    ) -> Subscribe | None:
        return await self.get((telegram_chat_id, github_repository_id))

    async def get_by_chat(self, *, telegram_chat_id: int) -> Sequence[Subscribe]:
        stmt = select(Subscribe).where(Subscribe.telegram_chat_id == telegram_chat_id)
        return (await self.session.scalars(stmt)).all()

    async def get_by_repository(
        self, *, github_repository_id: int
    ) -> Sequence[Subscribe]:
        stmt = select(Subscribe).where(
            Subscribe.github_repository_id == github_repository_id
        )
        return (await self.session.scalars(stmt)).all()
