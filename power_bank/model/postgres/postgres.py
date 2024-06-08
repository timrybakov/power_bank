from power_bank.di import di

from sqlalchemy.exc import NoResultFound


class PostgresSource:
    def __init__(self) -> None:
        self._src = di.di_container.unit_of_work_container.unit_of_work

    async def create(self, record):
        async with self._src as uow:
            uow.users.create(record)
            await uow.commit()

    async def get_user_by_phone_number(self, phone_number):
        try:
            async with self._src as uow:
                record = await uow.users.get_user_by_phone_number(phone_number)
                return record.scalar_one()
        except NoResultFound:
            return None
