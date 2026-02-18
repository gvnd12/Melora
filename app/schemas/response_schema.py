from pydantic import BaseModel

from .common_schema import BaseResponse


class BaseMessageResponse(BaseModel):
    message: str


class BaseUserSchema(BaseResponse):
    first_name: str
    last_name: str | None = None
    username: str
    email: str
    is_active: bool


class LoginResponse(BaseModel):
    access_token: str


class UserResponse(BaseModel):
    message: str
    data: BaseUserSchema
