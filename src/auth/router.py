from typing import Annotated

from auth.dependencies import (
    authentication_service,
    deactivation_account_service,
    get_access_token,
    reactivation_account_service,
    registration_service,
    reset_password_service,
    token_service,
)
from auth.schemas import (
    AccessTokenSchema,
    LoginUserSchema,
    RegisterUserSchema,
    UserDetailsSchema,
    UserSchema,
)
from auth.services import (
    AuthenticationService,
    DeactivationAccountService,
    ReactivationAccountService,
    RegistrationService,
    ResetPasswordService,
    TokenService,
)
from fastapi import APIRouter, Cookie, Depends, Response
from pydantic import EmailStr

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/", status_code=201)
async def register(
    register_data: RegisterUserSchema,
    registration_service: Annotated[RegistrationService, Depends(registration_service)],
) -> UserSchema:
    return await registration_service.register_user(register_data)


@router.get("/email-confirmation/{token}/", status_code=200)
async def confirm_email(
    token: str,
    registration_service: Annotated[RegistrationService, Depends(registration_service)],
) -> UserSchema:
    return await registration_service.confirm_email(token)


@router.post("/login/", status_code=200)
async def login(
    response: Response,
    login_data: LoginUserSchema,
    authentication_service: Annotated[
        AuthenticationService, Depends(authentication_service)
    ],
) -> AccessTokenSchema:
    tokens = await authentication_service.authenticate_user(login_data)

    cookies = [
        {
            "key": "refresh_token_uuid",
            "value": tokens.refresh_token_uuid,
            "httponly": True,
            "path": "/api/auth/refresh",
            "secure": True,
        },
        {
            "key": "refresh_token_uuid",
            "value": tokens.refresh_token_uuid,
            "path": "/api/auth/logout",
            "secure": True,
        },
    ]
    for cookie in cookies:
        response.set_cookie(**cookie)

    return tokens.access_token


@router.post("/refresh/", status_code=200)
async def refresh(
    response: Response,
    refresh_token_uuid: Annotated[str, Cookie()],
    user_details: UserDetailsSchema,
    token_service: Annotated[TokenService, Depends(token_service)],
) -> AccessTokenSchema:
    tokens = await token_service.renew_tokens(
        refresh_token_uuid, user_details.fingerprint
    )

    cookies = [
        {
            "key": "refresh_token_uuid",
            "value": tokens.refresh_token_uuid,
            "httponly": True,
            "path": "/api/auth/refresh",
            "secure": True,
        },
        {
            "key": "refresh_token_uuid",
            "value": tokens.refresh_token_uuid,
            "path": "/api/auth/logout",
            "secure": True,
        },
    ]
    for cookie in cookies:
        response.set_cookie(**cookie)

    return tokens.access_token


@router.get("/logout/", status_code=204)
async def logout(
    response: Response,
    access_token: Annotated[str, Depends(get_access_token)],
    refresh_token_uuid: Annotated[str, Cookie()],
    token_service: Annotated[TokenService, Depends(token_service)],
):
    await token_service.check_access_token(access_token)
    await token_service.delete_refresh_token(refresh_token_uuid=refresh_token_uuid)

    response.delete_cookie("refresh_token_uuid")


@router.get("/reset-password/", status_code=204)
async def forgot_password(
    email: EmailStr,
    reset_password_service: Annotated[
        ResetPasswordService, Depends(reset_password_service)
    ],
) -> None:
    await reset_password_service.send_reset_password_email(email)


@router.post("/reset-password/{token}/", status_code=204)
async def reset_password(
    token: str,
    new_password: str,
    reset_password_service: Annotated[
        ResetPasswordService, Depends(reset_password_service)
    ],
) -> None:
    await reset_password_service.reset_password(token, new_password)


@router.get("/reset-password/{token}/", status_code=200)
async def check_reset_password_token(
    token: str,
    reset_password_service: Annotated[
        ResetPasswordService, Depends(reset_password_service)
    ],
) -> None:
    await reset_password_service.check_reset_password_token(token)


@router.get("/deactivate/", status_code=204)
async def send_deactivation_account_email(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    deactivation_account_service: Annotated[
        DeactivationAccountService, Depends(deactivation_account_service)
    ],
) -> None:
    await token_service.check_access_token(access_token)
    await deactivation_account_service.send_deactivation_account_email(access_token)


@router.post("/deactivate/", status_code=204)
async def deactivate_account(
    access_token: Annotated[str, Depends(get_access_token)],
    token_service: Annotated[TokenService, Depends(token_service)],
    deactivation_account_service: Annotated[
        DeactivationAccountService, Depends(deactivation_account_service)
    ],
) -> None:
    await token_service.check_access_token(access_token)
    await deactivation_account_service.deactivate_account(access_token)


@router.get("/deactivate/{token}/", status_code=200)
async def check_deactivation_account_token(
    token: str,
    deactivation_account_service: Annotated[
        DeactivationAccountService, Depends(deactivation_account_service)
    ],
) -> None:
    await deactivation_account_service.check_deactivation_account_token(token)


@router.get("/reactivate/", status_code=204)
async def reactivate_account(
    email: EmailStr,
    reactivation_account_service: Annotated[
        ReactivationAccountService, Depends(reactivation_account_service)
    ],
) -> None:
    await reactivation_account_service.send_reactivation_account_email(email)


@router.post("/reactivate/", status_code=204)
async def reactivation_account(
    token: str,
    new_password: str,
    reactivation_account_service: Annotated[
        ReactivationAccountService, Depends(reactivation_account_service)
    ],
) -> None:
    await reactivation_account_service.reactivation_account(token, new_password)


@router.get("/reactivate/{token}/", status_code=200)
async def check_reactivation_account_token(
    token: str,
    reactivation_account_service: Annotated[
        ReactivationAccountService, Depends(reactivation_account_service)
    ],
) -> None:
    await reactivation_account_service.check_reactivation_account_token(token)
