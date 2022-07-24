# DATABASE FILE

from typing import List, Any
import asyncpg
from customs.log import AuroraLogger

db_logger = AuroraLogger("AuroraDBLog", "logs/db.log")


class AuroraDatabase:
    def __init__(self, database: str, user: str, password: str) -> None:
        self._pool = None
        self._db: str = database
        self._user: str = user
        self._password: str = password
        self._pool: asyncpg.pool.Pool

    async def create_conn(self):
        self._pool = await asyncpg.create_pool(database=self._db, user=self._user, password=self._password)
        print("connected")
        db_logger.info(f"Successfully connected to database {self._db}")
        await self._create_tables()

    async def execute(self, *args, **kwargs) -> None:
        return await self._pool.execute(*args, **kwargs)

    async def executemany(self, *args, **kwargs) -> None:
        return await self._pool.executemany(*args, **kwargs)

    async def fetch(self, *args, **kwargs) -> List[asyncpg.Record]:
        return await self._pool.fetch(*args, **kwargs)

    async def fetch_row(self, *args, **kwargs) -> asyncpg.Record:
        return await self._pool.fetchrow(*args, **kwargs)

    async def fetch_val(self, *args, **kwargs) -> Any:
        return await self._pool.fetchval(*args, **kwargs)

    async def _create_tables(self) -> None:
        # query = """CREATE TABLE IF NOT EXISTS disable_categories(
        #     guild_id integer PRIMARY KEY NOT NULL UNIQUE,
        #     disabled_extensions text[]
        # )"""
        query = None
        await self.execute(query)
