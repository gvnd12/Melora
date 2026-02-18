
from fastapi import APIRouter, HTTPException, status
from app.models.song_model import Songs
from app.schemas.song_schema import SongCreate
from app.services.recommendation_service import get_recommendations

song_router = APIRouter(tags=["song"], prefix="/api/song")

@song_router.post(path="/")
async def add_song(payload:SongCreate):
    song_data = payload.model_dump()
    response = await Songs().create_song(song_data=song_data)
    return response

@song_router.get(path="/recommendations")
async def get_songs(song_id:str):
    songs = await get_recommendations(song_id)
    return songs