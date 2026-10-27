from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import settings

engine = create_async_engine(settings.pg_url, echo=False, pool_pre_ping=True)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def check_db_connection():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except OperationalError as e:
        raise RuntimeError(
            f"Database is unavailable at {engine.url.host}:{engine.url.port}. Is PostgreSQL running?"
        ) from e
