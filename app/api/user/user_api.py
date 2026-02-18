from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from app.models.user_model import User
from app.schemas import BaseMessageResponse, CreateUserRequest, UserResponse

user_router = APIRouter(tags=["user"], prefix="/api/user")


@user_router.post(path="/", status_code=200, response_model=BaseMessageResponse)
async def create_user(payload: CreateUserRequest):
    try:
        user_details = payload.model_dump()

        response = await User().create_user_entry(user_details=user_details)
        return {"message": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.get(path="/{user_id}", status_code=200, response_model=UserResponse)
async def get_user(user_id: Annotated[str, Path()]):
    try:
        response = await User().get_user_details(user_id=user_id)
        data = response.get("data")
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )
        return {"message": response.get("message"), "data": data[0]}
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
