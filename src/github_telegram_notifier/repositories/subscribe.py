from collections.abc import Sequence

from sqlalchemy import select

from ..models import Subscribe
from .base import BaseRepository


class SubscribeRepository(BaseRepository[Subscribe]):
    model = Subscribe

    def create(
        self, *, telegram_chat_id: int, github_repository_id: int, title: str
    ) -> Subscribe:
        return self.add(
            Subscribe(
                telegram_chat_id=telegram_chat_id,
                github_repository_id=github_repository_id,
                title=title,
            )
        )

    def get_by_ids(
        self, *, telegram_chat_id: int, github_repository_id: int
    ) -> Subscribe | None:
        return self.get((telegram_chat_id, github_repository_id))

    def get_by_chat(self, *, telegram_chat_id: int) -> Sequence[Subscribe]:
        stmt = select(Subscribe).where(Subscribe.telegram_chat_id == telegram_chat_id)
        return self._all(stmt)

    def get_by_repository(self, *, github_repository_id: int) -> Sequence[Subscribe]:
        stmt = select(Subscribe).where(
            Subscribe.github_repository_id == github_repository_id
        )
        return self._all(stmt)
