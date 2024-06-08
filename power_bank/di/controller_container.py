from power_bank import clients, controller


class ControllerContainer:
    def __init__(self, settings, uow_container):
        self._settings = settings
        self.uow_container = uow_container

    @property
    def twilio_client(self):
        return clients.TwilioClient(
            twilio_account_sid=self._settings.twilio_account_sid,
            twilio_auth_token=self._settings.twilio_auth_token
        )

    @property
    def redis_client(self):
        return clients.RedisClient(
            host=self._settings.redis_host,
            port=self._settings.redis_port,
            db=self._settings.redis_db
        )

    @property
    def auth_controller(self):
        return controller.AuthController(
            settings=self._settings,
            client=self.twilio_client.get_twilio_client,
            redis=self.redis_client.get_redis,
            unit_of_work=self.uow_container.unit_of_work
        )
