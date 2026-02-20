from pydantic import BaseModel


class SongCreate(BaseModel):
    title: str
    artist: str
    genre: str
    lyrics: str | None = None
    source: str | None = None


class SongResponse(BaseModel):
    id: str
    title: str
    artist: str
    genre: str


class RecommendationResponse(BaseModel):
    recommendations: list[SongResponse]
