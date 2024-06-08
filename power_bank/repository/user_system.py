from sqlalchemy import select

from .sources.user_system import user_system_postgres
from ..model.database import User
from ..model.model_custom_errors import NotFoundExceptions


class UserSystem:
    def __init__(self, session) -> None:
        self._source = user_system_postgres.UserSystemPostgres(session=session)

    def create(self, record):
        self._source.add(record)

    async def get_user_by_phone_number(self, phone_number):
        try:
            stmt = select(User).filter(User.phone_number == phone_number)
            return await self._source.execute(stmt=stmt)
        except NotFoundExceptions:
            raise NotFoundExceptions

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
