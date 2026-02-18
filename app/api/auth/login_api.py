from fastapi import APIRouter, HTTPException, status

from app.models.user_model import User
from app.schemas import BaseMessageResponse, LoginRequest, LoginResponse

auth_router = APIRouter(tags=["auth"], prefix="/api")


@auth_router.post(path="/login", response_model=LoginResponse | BaseMessageResponse)
async def login_api(payload: LoginRequest):
    try:
        username = payload.username
        password = payload.password

        response = await User().read_entry(
            filter_domain={"username": username},
            projection={"username": True, "password": True},
        )
        data = response.get("data")
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
            )
        token = await User().authenticate(user=data[0], password=password)
        if token.get("error"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
