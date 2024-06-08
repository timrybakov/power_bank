import redis


class RedisClient:
    def __init__(self, host: str, port: int, db: int) -> None:
        self._host = host
        self._port = port
        self._db = db

    @property
    def get_redis(self):
        return redis.Redis(
            host=self._host, port=self._port, db=self._db
        )
