from app.core.config import settings
from app.database.vector_db import qdrant
from app.services.embedding_service import generate_embedding


async def create_song(song_data):
    song_dict = song_data.dict()

    result = await song_collection.insert_one(song_dict)
    song_id = str(result.inserted_id)

    # 2. Generate embedding
    text_for_embedding = f"{song_data.title} {song_data.artist} {song_data.genre} {song_data.lyrics or ''}"
    embedding = generate_embedding(text_for_embedding)

    # 3. Store in Qdrant
    qdrant.upsert(
        collection_name=settings.COLLECTION_NAME,
        points=[
            {
                "id": song_id,
                "vector": embedding,
                "payload": {"genre": song_data.genre, "artist": song_data.artist},
            }
        ],
    )

    return song_id
