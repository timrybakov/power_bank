from twilio.rest import Client


class TwilioClient:
    def __init__(self, twilio_account_sid: str, twilio_auth_token: str) -> None:
        self._twilio_account_sid = twilio_account_sid
        self._twilio_auth_token = twilio_auth_token

    @property
    def get_twilio_client(self):
        return Client(
            self._twilio_account_sid,
            self._twilio_auth_token
        )
