from .sources.machine_system import machine_system_postgres


class MachineSystem:
    def __init__(self, session) -> None:
        self._source = machine_system_postgres.MachineSystemPostgres(session=session)

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
