from typing import Annotated

from auth.services import (
    AuthenticationService,
    DeactivationAccountService,
    ReactivationAccountService,
    RegistrationService,
    ResetPasswordService,
    TokenService,
)
from fastapi import Header, HTTPException
from unit_of_work import UnitOfWork


def registration_service() -> RegistrationService:
    return RegistrationService(UnitOfWork)


def authentication_service() -> AuthenticationService:
    return AuthenticationService(UnitOfWork)


def token_service() -> TokenService:
    return TokenService(UnitOfWork)


def get_access_token(authorization: Annotated[str, Header()]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Incorrect header Authorization format"
        )

    access_token = authorization.replace("Bearer ", "")

    if not access_token:
        raise HTTPException(status_code=401, detail="No access token provided")

    return access_token


def reset_password_service() -> ResetPasswordService:
    return ResetPasswordService(UnitOfWork)


def deactivation_account_service() -> DeactivationAccountService:
    return DeactivationAccountService(UnitOfWork)


def reactivation_account_service() -> ReactivationAccountService:
    return ReactivationAccountService(UnitOfWork)
