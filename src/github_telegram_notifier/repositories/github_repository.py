from collections.abc import Sequence

from sqlalchemy import select

from ..models import Github_repository
from .base import BaseRepository


class GithubRepositoryRepository(BaseRepository[Github_repository]):
    model = Github_repository

    async def create(
        self, *, user_id: int, url: str, title: str | None = None
    ) -> Github_repository:
        return await self.add(Github_repository(user_id=user_id, url=url, title=title))

    async def get_by_url(self, url: str) -> Sequence[Github_repository]:
        stmt = select(Github_repository).where(Github_repository.url == url)
        return (await self.session.scalars(stmt)).all()

    async def get_by_user(self, user_id: int) -> Sequence[Github_repository]:
        stmt = select(Github_repository).where(Github_repository.user_id == user_id)
        return (await self.session.scalars(stmt)).all()
