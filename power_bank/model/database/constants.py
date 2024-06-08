import enum


class Status(enum.Enum):
    online = 'online'
    offline = 'offline'


class DefaultDataEnum(enum.Enum):
    phone_number_length = 20
    base_length = 256
    work_time_length = 16
    default_bonuses = 0
