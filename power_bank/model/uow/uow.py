from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from power_bank import repository, clients


class BaseDBUOW:
    def __init__(
        self,
        db_client: clients.PostgresClient,
        session: AsyncSession | None = None
    ) -> None:
        self._db_client = db_client
        self._session = session if session else self._db_client.create_session()
        self._db_repo_params = {
            "session": self._session,
            "db_client": db_client,
            "autocommit": False,
            "auto_flush": True,
        }

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def close_session(self) -> None:
        await self._session.close()


class BaseDBUOWContext:
    def __init__(
        self,
        db_client: clients.PostgresClient,
        session: AsyncSession | None = None
    ) -> None:
        self._uow: BaseDBUOW | None = None
        self._db_client = db_client
        self._session = session

    async def __aenter__(self) -> BaseDBUOW:
        self._uow = BaseDBUOW(
            db_client=self._db_client,
            session=self._session
        )
        return self._uow

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_val:
                await self._uow.rollback()
            else:
                await self._uow.commit()
        finally:
            await self._uow.close_session()


class UOW(BaseDBUOWContext):
    def __init__(
        self,
        db_client: clients.PostgresClient
    ) -> None:
        self._session = db_client.create_session()
        self.user_repo = repository.UserSystem(self._session)
        self.rent_repo = repository.RentalSystem(self._session)
        self.machine_repo = repository.MachineSystem(self._session)
        super().__init__(
            db_client=db_client,
            session=self._session
        )

    async def __aenter__(self):
        await super().__aenter__()
        self.users = self.user_repo
        self.rents = self.rent_repo
        self.machines = self.machine_repo
        return self

    async def commit(self) -> None:
        await self._uow.commit()

    async def rollback(self) -> None:
        await self._uow.rollback()

    async def close_session(self) -> None:
        await self._uow.close_session()
