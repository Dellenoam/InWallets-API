import uuid
from datetime import datetime, timedelta
from typing import Any, Type

from auth.schemas import (
    AccessTokenSchema,
    LoginUserSchema,
    RegisterUserSchema,
    TokensSchema,
    UserSchema,
)
from auth.tasks import (
    send_deactivation_account_link,
    send_email_confirmation_link,
    send_reactivation_account_link,
    send_reset_password_link,
)
from auth.utils import decode_jwt, encode_jwt, hash_password, validate_password_hash
from configs.config import serializer, settings
from database import async_session
from fastapi import HTTPException
from itsdangerous import BadSignature, SignatureExpired
from unit_of_work import UnitOfWork


class RegistrationService:
    def __init__(self, unit_of_work: Type[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work(async_session)

    async def register_user(self, user_data: RegisterUserSchema) -> UserSchema:
        async with self._unit_of_work as uow:
            if await uow.user.get_by(email=user_data.email):
                raise HTTPException(status_code=409, detail="User already exists")

            hashed_password = hash_password(user_data.password)
            user_data.password = hashed_password

            user = await uow.user.create(user_data.model_dump())

            send_email_confirmation_link.delay(user.email)

            await uow.commit()

        return UserSchema(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

    async def confirm_email(self, token: str) -> UserSchema:
        async with self._unit_of_work as uow:
            try:
                payload = serializer.loads(
                    token, salt=settings.crypto.SALT_EMAIL_CONFIRMATION, max_age=3600
                )
            except SignatureExpired:
                raise HTTPException(
                    status_code=404, detail="Confirmation link is expired"
                )
            except BadSignature:
                raise HTTPException(
                    status_code=404, detail="Confirmation link is invalid"
                )

            user = await uow.user.get_by(email=payload["email"])

            if not user:
                raise HTTPException(
                    status_code=404, detail="Confirmation link is invalid"
                )

            await uow.user.update(user, {"is_verified": True})

            await uow.commit()

        return UserSchema(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )


class AuthenticationService:
    def __init__(self, unit_of_work: Type[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work(async_session)
        self._token_service = TokenService(unit_of_work)

    async def authenticate_user(self, user: LoginUserSchema) -> TokensSchema:
        async with self._unit_of_work as uow:
            user_from_db = await uow.user.get_by(email=user.email)

            if not user_from_db or not validate_password_hash(
                user.password, user_from_db.password
            ):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            if not user_from_db.is_active:
                raise HTTPException(status_code=403, detail="User is inactive")

            if not user_from_db.is_verified:
                raise HTTPException(
                    status_code=403, detail="User has not confirmed email"
                )

            tokens = await self._token_service.create_tokens(
                user_from_db.id, user_from_db.email, user.user_details.fingerprint
            )

            return tokens


class TokenService:
    def __init__(self, unit_of_work: Type[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work(async_session)
        self._token_generator = TokenGenerator()

    async def create_tokens(
        self, user_id: int, user_email: str, fingerprint: str
    ) -> TokensSchema:
        async with self._unit_of_work as uow:
            access_token = await self._token_generator.generate_access_token(
                user_id, user_email
            )
            refresh_token = await self._token_generator.generate_refresh_token(
                uow, user_id, user_email, fingerprint
            )

            await uow.commit()

        return TokensSchema(access_token=access_token, refresh_token_uuid=refresh_token)

    async def renew_tokens(
        self, refresh_token_uuid: str, fingerprint: str
    ) -> TokensSchema:
        async with self._unit_of_work as uow:
            refresh_token = await uow.refresh_token.get_by(
                refresh_token_uuid=refresh_token_uuid
            )

            if not refresh_token:
                raise HTTPException(status_code=401, detail="Refresh token not found")

            await uow.refresh_token.delete(refresh_token)

            if (
                refresh_token.exp < int(datetime.now().timestamp())
                or not refresh_token.fingerprint == fingerprint
            ):
                raise HTTPException(status_code=403, detail="Invalid refresh token")

            access_token = await self._token_generator.generate_access_token(
                refresh_token.sub, refresh_token.email
            )
            refresh_token_uuid = await self._token_generator.generate_refresh_token(
                uow, refresh_token.sub, refresh_token.email, fingerprint
            )

            await uow.commit()

            return TokensSchema(
                access_token=access_token, refresh_token_uuid=refresh_token_uuid
            )

    async def check_access_token(self, access_token: str) -> dict[str, Any]:
        payload = decode_jwt(access_token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid access token")

        if payload["exp"] < int(datetime.now().timestamp()):
            raise HTTPException(status_code=403, detail="Access token expired")

        user_data = {
            "id": payload["sub"],
            "email": payload["email"],
            "scopes": payload["scopes"],
        }

        return user_data

    async def delete_refresh_token(self, refresh_token_uuid: str) -> None:
        async with self._unit_of_work as uow:
            refresh_token = await uow.refresh_token.get_by(
                refresh_token_uuid=refresh_token_uuid
            )

            if not refresh_token:
                raise HTTPException(status_code=401, detail="Refresh token not found")

            await uow.refresh_token.delete(refresh_token)

            await uow.commit()


class TokenGenerator:
    async def generate_access_token(
        self, user_id: int, user_email: str
    ) -> AccessTokenSchema:
        iat = datetime.now()
        exp = datetime.now() + timedelta(
            minutes=settings.token.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": user_id,
            "email": user_email,
            "scopes": [],
            "iat": int(iat.timestamp()),
            "exp": int(exp.timestamp()),
        }

        access_token = encode_jwt(payload)

        access_token = AccessTokenSchema(token=access_token)

        return access_token

    async def generate_refresh_token(
        self, uow: UnitOfWork, user_id: int, user_email: str, fingerprint: str
    ) -> str:
        refresh_token_uuid = str(uuid.uuid4())
        iat = datetime.now()
        exp = datetime.now() + timedelta(days=settings.token.REFRESH_TOKNE_EXPIRE_DAYS)

        payload = {
            "sub": user_id,
            "email": user_email,
            "fingerprint": fingerprint,
            "refresh_token_uuid": refresh_token_uuid,
            "iat": int(iat.timestamp()),
            "exp": int(exp.timestamp()),
        }

        await uow.refresh_token.create(payload)

        return refresh_token_uuid

    async def delete_refresh_token(
        self, uow: UnitOfWork, refresh_token_uuid: str
    ) -> None:
        refresh_token = await uow.refresh_token.get_by(
            refresh_token_uuid=refresh_token_uuid
        )

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token not found")

        await uow.refresh_token.delete(refresh_token)


class ResetPasswordService:
    def __init__(self, unit_of_work: Type[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work(async_session)

    async def send_reset_password_email(self, email: str) -> None:
        send_reset_password_link.delay(email)

    async def check_reset_password_token(self, token: str) -> None:
        try:
            serializer.loads(
                token, salt=settings.crypto.SALT_RESET_PASSWORD, max_age=3600
            )
        except SignatureExpired:
            raise HTTPException(
                status_code=404, detail="Reset password link is expired"
            )
        except BadSignature:
            raise HTTPException(
                status_code=404, detail="Reset password link is invalid"
            )

    async def reset_password(self, token: str, new_password: str) -> None:
        async with self._unit_of_work as uow:
            try:
                payload = serializer.loads(
                    token, salt=settings.crypto.SALT_RESET_PASSWORD, max_age=3600
                )
            except SignatureExpired:
                raise HTTPException(
                    status_code=404, detail="Reset password link is expired"
                )
            except BadSignature:
                raise HTTPException(
                    status_code=404, detail="Reset password link is invalid"
                )

            user = await uow.user.get_by(email=payload["email"])

            if not user:
                raise HTTPException(
                    status_code=404, detail="Reset password link is invalid"
                )

            if validate_password_hash(new_password, user.password):
                raise HTTPException(
                    status_code=400,
                    detail="New password must be different from current password",
                )

            new_password = hash_password(new_password)

            await uow.user.update(user, {"password": new_password})

            await uow.commit()


class DeactivationAccountService:
    def __init__(self, unit_of_work: Type[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work(async_session)

    async def send_deactivation_account_email(self, email: str) -> None:
        send_deactivation_account_link.delay(email)

    async def check_deactivation_account_token(self, token: str) -> None:
        try:
            serializer.loads(
                token, salt=settings.crypto.SALT_DEACTIVATION_ACCOUNT, max_age=3600
            )
        except SignatureExpired:
            raise HTTPException(status_code=404, detail="Deactivation link is expired")
        except BadSignature:
            raise HTTPException(status_code=404, detail="Deactivation link is invalid")

    async def deactivate_account(self, token: str) -> None:
        async with self._unit_of_work as uow:
            try:
                payload = serializer.loads(
                    token, salt=settings.crypto.SALT_DEACTIVATION_ACCOUNT, max_age=3600
                )
            except SignatureExpired:
                raise HTTPException(
                    status_code=404, detail="Deactivation link is expired"
                )
            except BadSignature:
                raise HTTPException(
                    status_code=404, detail="Deactivation link is invalid"
                )

            user = await uow.user.get_by(email=payload["email"])

            if not user:
                raise HTTPException(
                    status_code=404, detail="Deactivation link is invalid"
                )

            await uow.user.update(user, {"is_active": False})

            await uow.commit()


class ReactivationAccountService:
    def __init__(self, unit_of_work: Type[UnitOfWork]) -> None:
        self._unit_of_work = unit_of_work(async_session)

    async def send_reactivation_account_email(self, email: str) -> None:
        send_reactivation_account_link.delay(email)

    async def check_reactivation_account_token(self, token: str) -> None:
        try:
            serializer.loads(
                token,
                salt=settings.crypto.SALT_REACTIVATION_ACCOUNT,
                max_age=3600,
            )
        except SignatureExpired:
            raise HTTPException(status_code=404, detail="Reactivation link is expired")
        except BadSignature:
            raise HTTPException(status_code=404, detail="Reactivation link is invalid")

    async def reactivation_account(self, token: str, new_password: str) -> None:
        async with self._unit_of_work as uow:
            try:
                payload = serializer.loads(
                    token,
                    salt=settings.crypto.SALT_REACTIVATION_ACCOUNT,
                    max_age=3600,
                )
            except SignatureExpired:
                raise HTTPException(
                    status_code=404, detail="Reactivation link is expired"
                )
            except BadSignature:
                raise HTTPException(
                    status_code=404, detail="Reactivation link is invalid"
                )

            user = await uow.user.get_by(email=payload["email"])

            if not user:
                raise HTTPException(
                    status_code=404, detail="Reactivation link is invalid"
                )

            if validate_password_hash(new_password, user.password):
                raise HTTPException(
                    status_code=400,
                    detail="New password must be different from current password",
                )

            new_password = hash_password(new_password)

            await uow.user.update(user, {"password": new_password, "is_active": True})

            await uow.user.update(user, {"is_active": True})

            await uow.commit()
