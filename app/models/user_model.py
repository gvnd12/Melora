
import logging

from app.core.config import settings
from app.core.jwt_manager import _encode_jwt
from app.database import MongoDB
from app.tools.utils import password_hash, verify_password

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class User(MongoDB):
    collection_name = settings.MONGO_USER_COLLECTION

    __slots__ = (
        "first_name",
        "last_name",
        "username",
        "email",
        "password",
        "is_active",
        "is_deleted",
    )

    def __init__(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        is_active: bool | None = None,
        is_deleted: bool | None = None,
    ):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.is_active = is_active
        self.is_deleted = is_deleted

    async def authenticate(self, user: dict, password: str):
        is_verified = verify_password(plain_pass=password, hashed_pass=user["password"])
        if not is_verified:
            return {"error": "Invalid username or password"}
        token_payload = {"username": user["username"], "password": user["password"]}
        return {"access_token": _encode_jwt(context=token_payload)}

    async def create_user_entry(self, user_details: dict):
        user_details["password"] = password_hash(user_details["password"])
        user_details["is_active"] = True

        _, result = await self.write_entry(document=user_details)

        logger.info(msg=f"User {user_details.get('username')} created successfully.")
        return result

    async def get_user_details(self, user_id: str):
        user = await self.read_entry(
            filter_domain={"_id": user_id}, projection={"password": False}
        )
        return user
