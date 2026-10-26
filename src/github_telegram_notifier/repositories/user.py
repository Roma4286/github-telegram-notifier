from sqlalchemy import select

from ..models import User, UserRole
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    def create(
        self, *, username: str, password: str, role: UserRole = UserRole.USER
    ) -> User:
        return self.add(User(username=username, password=password, role=role))

    def get_by_username(self, username: str) -> User | None:
        return self._first(select(User).where(User.username == username))
