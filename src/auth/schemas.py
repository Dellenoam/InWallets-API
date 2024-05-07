import re

from pydantic import BaseModel, EmailStr, Field, validator


class UserSchema(BaseModel):
    id: int
    email: EmailStr = Field(examples=["username@example.com"])
    is_active: bool = Field(examples=[True])
    is_verified: bool = Field(examples=[False])


class RegisterUserSchema(BaseModel):
    email: EmailStr = Field(examples=["username@example.com"])
    password: str = Field(examples=["StrongPassword123!"])

    @validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search("[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search("[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search("[0-9]", password):
            raise ValueError("Password must contain at least one digit")

        if not re.search("[!@#$%^&*()_+{}:<>?]", password):
            raise ValueError("Password must contain at least one special character")

        return password


class AccessTokenSchema(BaseModel):
    token: str = Field(
        examples=[
            "header.payload.signature",
        ]
    )
    token_type: str = Field(examples=["Bearer"], default="Bearer")


class TokensSchema(BaseModel):
    access_token: AccessTokenSchema = Field(examples=["header.payload.signature"])
    refresh_token_uuid: str = Field(examples=["refresh_token_uuid"])


class UserDetailsSchema(BaseModel):
    fingerprint: str = Field(examples=["fingerprint"])


class LoginUserSchema(BaseModel):
    email: EmailStr = Field(examples=["username@example.com"])
    password: str = Field(examples=["StrongPassword123!"])
    user_details: UserDetailsSchema
