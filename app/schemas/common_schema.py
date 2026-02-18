from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    id: str = Field(alias="_id")
    is_deleted: bool
    created_at: int
    updated_at: int | None = None
