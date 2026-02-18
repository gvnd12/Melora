from app.core.config import settings
from app.database.vector_db import qdrant
from app.database import MongoDB
from app.models.song_model import Songs
import uuid

async def get_recommendations(song_id:str):
    point = qdrant.retrieve(
        collection_name=settings.QDRANT_SONGS_COLLECTION,
        ids=[song_id],
        with_vectors=True
    )

    if not point:
        return []

    vector = point[0].vector

    results = qdrant.query_points(
        collection_name=settings.QDRANT_SONGS_COLLECTION,
        query=vector,
        limit=3,
    )
    recommendations = []
    for result in results.points:
        if str(uuid.UUID(result.id).hex)==song_id:
            continue
        record = await Songs().read_entry(filter_domain={"_id":str(uuid.UUID(result.id).hex)})
        song_list = record["data"]
        song = song_list[0]
        if song:
            recommendations.append(
                {
                    "id":str(song.get("_id")),
                    "artist": str(song.get("artist")),
                    "genre": str(song.get("genre")),
                    "title": str(song.get("title")),
                }
            )

    return recommendations