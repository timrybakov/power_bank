from pydantic import BaseModel, Field

from ..database import constants


class User(BaseModel):
    phone_number: str = Field(max_length=constants.DefaultDataEnum.phone_number_length.value)


class UserLogin(User):
    password: str


class UserWithVerifCode(UserLogin):
    verif_code: str


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    phone_number: str
