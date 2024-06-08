import asyncio
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import jwt

from ..controller import constants
from ..model import schemes
from power_bank.model.database import User
from power_bank.model.model_custom_errors import NotFoundExceptions


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthController:
    def __init__(
            self,
            settings,
            client,
            redis,
            unit_of_work
    ) -> None:
        self._client = client
        self._settings = settings
        self._redis = redis
        self.unit_of_work = unit_of_work

    def _create_access_token(
            self,
            data: dict,
            expires_delta: timedelta | None = None
    ) -> jwt:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update(
            {
                "exp": expire
            }
        )
        encoded_jwt = jwt.encode(
            to_encode, self._settings.secret_key,
            algorithm=self._settings.algorithm
        )
        return encoded_jwt

    def _verify_password(
            self,
            plain_password: str,
            hashed_password: str
    ) -> CryptContext:
        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    def _get_code(self) -> secrets:
        return secrets.token_hex(3)

    def _send_sms(
            self,
            to_number: str,
            body: str
    ):
        return self._client.messages.create(
            from_=self._settings.twilio_phone_number,
            to=to_number, body=body
        )

    def _decode_binary(
            self,
            data: bytes
    ) -> str:
        return data.decode(
            constants.TokenEnum.encoding.value
        )

    def _get_hash_password(
            self,
            password: str
    ) -> CryptContext:
        return pwd_context.hash(password)

    async def _check_user_exists(
            self,
            phone_number: str
    ) -> User | None:
        try:
            async with self.unit_of_work as uow:
                user = await uow.users.get_user_by_phone_number(phone_number=phone_number)
                return user
        except NotFoundExceptions:
            return None

    async def authenticate_user(
            self,
            phone_number: str,
            password: str
    ) -> CryptContext:
        try:
            async with self.unit_of_work as uow:
                user = await uow.users.get_user_by_phone_number(
                    phone_number=phone_number
                )
                if not self._verify_password(
                        plain_password=password,
                        hashed_password=user.hashed_password
                ):
                    raise NotFoundExceptions
                access_token_expires = timedelta(
                    minutes=constants.TokenEnum.access_token_expire_minutes.value
                )
                access_token = self._create_access_token(
                    data={
                        "sub": user.phone_number
                    },
                    expires_delta=access_token_expires
                )
                return access_token
        except NotFoundExceptions:
            raise NotFoundExceptions

    async def signin_for_access_token(
            self,
            user_signin_data: schemes.UserLogin
    ) -> schemes.Token:
        try:
            access_token = await self.authenticate_user(
                phone_number=user_signin_data.phone_number,
                password=user_signin_data.password
            )
            return schemes.Token(
                access_token=access_token,
                token_type="bearer"
            )
        except NotFoundExceptions:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect phone number or password.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

    async def check_new_user(
            self,
            user_signup_data: schemes.UserLogin
    ) -> JSONResponse:
        user = await self._check_user_exists(
            user_signup_data.phone_number
        )
        if user:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="User already exists.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )
        auth_code = self._get_code()
        await asyncio.get_event_loop().run_in_executor(
            None,
            self._send_sms,
            user_signup_data.phone_number,
            auth_code
        )
        self._redis.set(
            user_signup_data.phone_number,
            auth_code
        )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                'message': 'Unregistered user.'
            }
        )

    async def check_authentication_code(
            self,
            user_verifying_data: schemes.UserWithVerifCode
    ) -> JSONResponse:
        auth_code = self._decode_binary(
            self._redis.get(
                user_verifying_data.phone_number
            )
        )
        if auth_code != user_verifying_data.verif_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect verification code.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )
        async with self.unit_of_work as uow:
            uow.users.create(
                User(
                    phone_number=user_verifying_data.phone_number,
                    hashed_password=self._get_hash_password(
                        user_verifying_data.password
                    )
                )
            )
            await uow.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                'message': 'User successfully created.'
            }
        )
