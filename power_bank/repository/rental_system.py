from .sources.rental_system import rental_system_postgres


class RentalSystem:
    def __init__(self, session) -> None:
        self._source = rental_system_postgres.RentalSystemPostgres(session=session)

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
