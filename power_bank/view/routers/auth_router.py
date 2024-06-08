from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse, FileResponse

from power_bank.di import di
from power_bank.model import schemes

__all__ = ['router']

router = APIRouter(
    tags=['registration and authorization']
)


@router.post('/signin')
async def signin_for_access_token(
    user_signin_data: schemes.UserLogin,
) -> schemes.Token:
    return await di.di_container.controller_container.auth_controller.signin_for_access_token(
        user_signin_data
    )


@router.post('/signup')
async def signup(
    user_signup_data: schemes.UserLogin
) -> JSONResponse:
    return await di.di_container.controller_container.auth_controller.check_new_user(
        user_signup_data
    )


@router.post('/signup/phone-number-verification')
async def phone_number_verification(
        user_verifying_data: schemes.UserWithVerifCode
) -> JSONResponse:
    return await di.di_container.controller_container.auth_controller.check_authentication_code(
        user_verifying_data
    )
