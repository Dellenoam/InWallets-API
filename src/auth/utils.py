from typing import Any, Dict

import bcrypt
import jwt
from configs.config import settings


def encode_jwt(
    payload: Dict[str, Any],
    private_key: str = settings.crypto.PRIVATE_KEY_PATH.read_text(),
    algorithm: str = settings.crypto.ALGORITHM,
) -> str:
    return jwt.encode(payload, private_key, algorithm)


def decode_jwt(
    token: str | bytes,
    publick_key: str = settings.crypto.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.crypto.ALGORITHM,
) -> Dict[str, Any] | None:
    try:
        return jwt.decode(token, publick_key, algorithms=[algorithm])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def validate_password_hash(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
