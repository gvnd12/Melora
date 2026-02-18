from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
