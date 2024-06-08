from datetime import datetime
from typing import Annotated

from sqlalchemy import String, ForeignKey, text, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase

from . import constants


intpk = Annotated[int, mapped_column(primary_key=True)]
user_status = Annotated[bool, mapped_column(default=False)]
time_update = Annotated[datetime, mapped_column(
        server_default=text('CURRENT_TIMESTAMP')
    )]
default_str_type = Annotated[str, mapped_column(
        String(constants.DefaultDataEnum.base_length.value), nullable=False
    )]
coordinates = Annotated[float, mapped_column(nullable=False)]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('idx_phone_number', 'phone_number'),
    )

    id: Mapped[intpk]
    phone_number: Mapped[str] = mapped_column(
        String(constants.DefaultDataEnum.phone_number_length.value),
        nullable=False, unique=True
    )
    bonuses: Mapped[int] = mapped_column(
        default=constants.DefaultDataEnum.default_bonuses.value
    )
    registered_at: Mapped[time_update]
    hashed_password: Mapped[default_str_type]
    is_superuser: Mapped[user_status]
    is_admin: Mapped[user_status]
    is_subscriber: Mapped[user_status]
    rents = relationship('Rent', back_populates='users')


class Rent(Base):
    __tablename__ = 'rents'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL')
    )
    users: Mapped[User] = relationship(
        back_populates='rents'
    )
    tariff: Mapped[default_str_type]
    rent_start_time: Mapped[time_update]
    rent_end_time: Mapped[time_update]
    price: Mapped[int] = mapped_column(nullable=False)


class Machine(Base):
    __tablename__ = 'machines'
    __table_args__ = (
        Index('idx_serial_number', 'serial_number'),
        Index('idx_status', 'status')
    )

    id: Mapped[intpk]
    serial_number: Mapped[int] = mapped_column(
        unique=True, nullable=False
    )
    latitude: Mapped[coordinates]
    longitude: Mapped[coordinates]
    work_time: Mapped[str] = mapped_column(
        String(constants.DefaultDataEnum.work_time_length.value)
    )
    register_time: Mapped[time_update]
    status: Mapped[constants.Status]
