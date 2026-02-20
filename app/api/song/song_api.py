from fastapi import APIRouter, UploadFile, File, Path
from app.models.song_model import Songs
from app.schemas.song_schema import SongCreate
from typing import Annotated

song_router = APIRouter(tags=["song"], prefix="/api/song")


@song_router.post(path="/")
async def add_song(payload: SongCreate):
    song_data = payload.model_dump()
    response = await Songs().create_song(song_data=song_data)
    return response


@song_router.get(path="/recommendations/{song_id}")
async def get_songs(song_id: Annotated[str, Path()]):
    songs = await Songs().get_recommendations(song_id)
    return songs


@song_router.post(path="/from_csv")
async def add_song_from_csv(file: UploadFile = File(...)):
    return await Songs().populate_db_from_csv(file)
