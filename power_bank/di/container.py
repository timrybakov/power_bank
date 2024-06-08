from functools import cached_property

from ..config import config
from .uow_container import UnitOfWorkContainer
from .controller_container import ControllerContainer


class Container:
    @cached_property
    def settings(self) -> config.Settings:
        return config.Settings()

    @property
    def unit_of_work_container(self):
        return UnitOfWorkContainer(self.settings)

    @cached_property
    def controller_container(self):
        return ControllerContainer(
            settings=self.settings,
            uow_container=self.unit_of_work_container
        )
