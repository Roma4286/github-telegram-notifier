from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .security import hash_password, verify_password


class Base(DeclarativeBase):
    pass


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    def __init__(self, username: str, password: str, role: UserRole = UserRole.USER):
        self.username = username
        self.password_hash = hash_password(password)
        self.role = role

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    telegram_chats: Mapped[list[Telegram_chat]] = relationship(
        "Telegram_chat",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    github_repositories: Mapped[list[Github_repository]] = relationship(
        "Github_repository",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)


class Telegram_chat(Base):
    __tablename__ = "telegram_chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column()
    title: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship("User", back_populates="telegram_chats")
    subscriptions: Mapped[list[Subscribe]] = relationship(
        "Subscribe",
        back_populates="telegram_chat",
        cascade="all, delete-orphan",
    )


class Github_repository(Base):
    __tablename__ = "github_repositories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None] = mapped_column()
    url: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship("User", back_populates="github_repositories")
    subscriptions: Mapped[list[Subscribe]] = relationship(
        "Subscribe",
        back_populates="github_repository",
        cascade="all, delete-orphan",
    )


class Subscribe(Base):
    __tablename__ = "subscriptions"

    telegram_chat_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_chats.id", ondelete="CASCADE"),
        primary_key=True,
    )
    github_repository_id: Mapped[int] = mapped_column(
        ForeignKey("github_repositories.id", ondelete="CASCADE"),
        primary_key=True,
    )

    telegram_chat: Mapped[Telegram_chat] = relationship(
        "Telegram_chat",
        back_populates="subscriptions",
    )
    github_repository: Mapped[Github_repository] = relationship(
        "Github_repository",
        back_populates="subscriptions",
    )

    title: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
