from sqlalchemy.exc import NoResultFound

from power_bank.model.model_custom_errors import NotFoundExceptions


class UserSystemPostgres:
    def __init__(self, session) -> None:
        self._session = session

    def add(self, record):
        self._session.add(record)

    async def execute(self, stmt):
        try:
            values = await self._session.execute(stmt)
            return values.scalar_one()
        except NoResultFound as error:
            print(error)
            raise NotFoundExceptions

    def update(self):
        pass

    def delete(self):
        pass
