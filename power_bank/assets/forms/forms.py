from fastapi.param_functions import Form

from typing_extensions import Annotated


class OAuth2PasswordRequestForm:

    def __init__(
        self,
        *,
        phone_number: Annotated[str, Form()],
        password: Annotated[str, Form()]
    ):
        self.phone_number = phone_number
        self.password = password
