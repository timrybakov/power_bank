import contextlib
from typing import Callable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@contextlib.asynccontextmanager
async def get_session_context(
    create_session_callback: Callable,
    session: AsyncSession | None = None,
    autocommit: bool = False,
    auto_flush: bool = False,
) -> AsyncSession:
    handling_session = session if session else create_session_callback()
    try:
        yield handling_session
    finally:
        if auto_flush:
            await handling_session.flush()
        if autocommit:
            await handling_session.commit()
        if not session:
            await handling_session.close()


class PostgresClient:
    _PING_QUERY = text("SELECT 1")

    def __init__(self, db_url: str) -> None:
        self._db_url = db_url
        self._async_engine = create_async_engine(self._db_url)
        self._session_maker = async_sessionmaker(
            autoflush=False,
            bind=self._async_engine,
            expire_on_commit=False
        )

    def create_session(self) -> AsyncSession:
        return self._session_maker()

    async def check_connection(self) -> bool:
        async with get_session_context(
            create_session_callback=self.create_session
        ) as session:
            with contextlib.suppress(Exception):
                ping_query_result = await session.execute(self._PING_QUERY)
                return bool(ping_query_result.fetchone())
        return False
