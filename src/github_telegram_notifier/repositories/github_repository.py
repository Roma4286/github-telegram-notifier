from collections.abc import Sequence

from sqlalchemy import select

from ..models import Github_repository
from .base import BaseRepository


class GithubRepositoryRepository(BaseRepository[Github_repository]):
    model = Github_repository

    def create(
        self, *, user_id: int, url: str, title: str | None = None
    ) -> Github_repository:
        return self.add(Github_repository(user_id=user_id, url=url, title=title))

    def get_by_url(self, url: str) -> Sequence[Github_repository]:
        stmt = select(Github_repository).where(Github_repository.url == url)
        return self._all(stmt)

    def get_by_user(self, user_id: int) -> Sequence[Github_repository]:
        stmt = select(Github_repository).where(Github_repository.user_id == user_id)
        return self._all(stmt)
