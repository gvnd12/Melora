from pydantic import BaseModel
from typing import List, Optional

class SongCreate(BaseModel):
    title: str
    artist: str
    genre: str
    lyrics: Optional[str] = None

class SongResponse(BaseModel):
    id: str
    title: str
    artist: str
    genre: str

class RecommendationResponse(BaseModel):
    recommendations: List[SongResponse]
