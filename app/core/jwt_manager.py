from datetime import datetime, timedelta

from jose import jwt

from .config import settings

now = datetime.now()
expire_delta = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))


def _encode_jwt(context: dict):
    return jwt.encode(
        claims={"iat": now, "exp": now + expire_delta, "context": context},
        key=str(settings.SECRET_KEY),
        algorithm=settings.JWT_ALGORITHM,
    )


def _decode_jwt(token: str):
    return jwt.decode(
        token=token, algorithms=settings.JWT_ALGORITHM, key=settings.SECRET_KEY
    )
