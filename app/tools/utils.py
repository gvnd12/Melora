import uuid

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_uuid():
    return str(uuid.uuid4().hex)


def password_hash(password: str):
    return pwd_context.hash(secret=password)


def verify_password(plain_pass: str, hashed_pass: str):
    return pwd_context.verify(secret=plain_pass, hash=hashed_pass)
