import asyncio

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(memory_cost=19456, time_cost=2, parallelism=1)


def _verify(password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except VerifyMismatchError:
        return False


# argon2 is CPU-bound, so it runs in a thread to keep the event loop free
async def hash_password(password: str) -> str:
    return await asyncio.to_thread(ph.hash, password)


async def verify_password(password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(_verify, password, hashed_password)
