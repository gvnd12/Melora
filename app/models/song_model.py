from app.core.config import settings
from app.database import MongoDB
from app.database.vector_db import qdrant
from app.services.embedding_service import generate_song_embeddings


class Songs(MongoDB):
    collection_name = settings.MONGO_SONGS_COLLECTION

    def __init__(self):
        super().__init__()

    async def create_song(self, song_data: dict):
        mongo_result, response = await self.write_entry(document=song_data)
        song_id = mongo_result.inserted_id

        song_text = f"{song_data.get('title')} {song_data.get('artist')} {song_data.get('genre')} {song_data.get('lyrics')}"
        embedding = generate_song_embeddings(song_data=song_text)

        qdrant.upsert(
            collection_name=settings.QDRANT_SONGS_COLLECTION,
            points=[
                {
                    "id": song_id,
                    "vector": embedding,
                    "payload": {
                        "genre": song_data.get("genre"),
                        "artist": song_data.get("artist"),
                    },
                }
            ],
        )

        return response
