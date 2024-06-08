from power_bank import clients
from power_bank.model.uow import uow


class UnitOfWorkContainer:
    def __init__(self, settings) -> None:
        self._settings = settings

    @property
    def postgres_client(self):
        return clients.PostgresClient(
            db_url=self._settings.db_url
        )

    @property
    def unit_of_work(self):
        return uow.UOW(
            db_client=self.postgres_client
        )
