import asyncio
import sys

from passlib.context import CryptContext

from core.user.user_repository import UserRepository
from utils.connection_pool import ConnectionPool

crypt_context = CryptContext(schemes=["sha256_crypt"])


async def main(email: str, plain_password: str) -> None:
    async with ConnectionPool.get_db_session() as session:
        user = await UserRepository().find_by_email(email=email, session=session)

    if user is None:
        print("user_not_found")
        return

    is_valid = crypt_context.verify(plain_password, user.password)
    print(f"hash={user.password}")
    print(f"password_valid={is_valid}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: py scripts\\check_user_password.py <email> <password>")
        sys.exit(1)

    asyncio.run(main(sys.argv[1], sys.argv[2]))