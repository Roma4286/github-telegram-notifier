from sqlalchemy import select

from ..models import User, UserRole
from ..security import hash_password
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def create(
        self, *, username: str, password: str, role: UserRole = UserRole.USER
    ) -> User:
        password_hash = await hash_password(password)
        return await self.add(
            User(username=username, password_hash=password_hash, role=role)
        )

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return (await self.session.scalars(stmt)).first()
