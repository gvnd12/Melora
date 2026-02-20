from app.core.config import settings
from app.database import MongoDB
from app.database.vector_db import qdrant
from app.services.embedding_service import generate_song_embeddings, model
import uuid
import csv
import io
from fastapi import UploadFile

from app.tools.utils import generate_uuid

BATCH_SIZE = 100
QDRANT_BATCH_SIZE = 500


class Songs(MongoDB):
    collection_name = settings.MONGO_SONGS_COLLECTION

    def __init__(
        self,
        qdrant_client: qdrant = qdrant,
        qdrant_collection: str = settings.QDRANT_SONGS_COLLECTION,
    ):
        super().__init__()
        self.qdrant = qdrant_client
        self.qdrant_collection = qdrant_collection

    async def create_song(self, song_data: dict):
        mongo_result, response = await self.write_entry(document=song_data)
        song_id = mongo_result.inserted_id

        song_text = f"{song_data.get('title')} {song_data.get('artist')} {song_data.get('genre')} {song_data.get('lyrics')}"
        embedding = generate_song_embeddings(song_data=song_text)

        self.qdrant.upsert(
            collection_name=self.qdrant_collection,
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

    async def get_recommendations(self, song_id: str):
        point = self.qdrant.retrieve(
            collection_name=self.qdrant_collection,
            ids=[song_id],
            with_vectors=True,
        )

        if not point:
            return []

        vector = point[0].vector

        results = self.qdrant.query_points(
            collection_name=settings.QDRANT_SONGS_COLLECTION,
            query=vector,
            limit=5,
        )

        recommendations = []
        for result in results.points:
            id_hex = str(uuid.UUID(result.id).hex)

            if id_hex == song_id:
                continue
            record = await self.read_entry(filter_domain={"_id": id_hex})
            song_list = record["data"]
            song = song_list[0]
            if song:
                recommendations.append(
                    {
                        "id": str(song.get("_id")),
                        "artist": str(song.get("artist")),
                        "genre": str(song.get("genre")),
                        "title": str(song.get("title")),
                        "source": str(song.get("source")),
                    }
                )

        return recommendations

    async def populate_db_from_csv(self, file: UploadFile):
        if not file.filename.endswith(".csv"):
            return {"message": "Only CSV files are allowed"}

        inserted_count = 0

        stream = io.TextIOWrapper(file.file, encoding="utf-8")
        reader = csv.DictReader(stream)

        batch = []

        for row in reader:
            batch.append(
                {
                    "_id": generate_uuid(),
                    "title": row.get("title"),
                    "artist": row.get("artist"),
                    "genre": row.get("genre"),
                    "lyrics": row.get("lyrics"),
                    "source": row.get("source"),
                }
            )

        if len(batch) >= BATCH_SIZE:
            inserted = await self._process_batch(batch)
            inserted_count += inserted
            batch = []

        if batch:
            inserted = await self._process_batch(batch)
            inserted_count += inserted

        return {"inserted": inserted_count}

    async def _process_batch(self, songs: list[dict]) -> int:
        if not songs:
            return 0

        titles = [s["title"] for s in songs]
        artists = [s["artist"] for s in songs]

        existing = await self.collection.find(
            {"$or": [{"title": {"$in": titles}, "artist": {"$in": artists}}]}
        ).to_list(length=None)

        existing_set = {(doc["title"], doc["artist"]) for doc in existing}

        new_songs = [s for s in songs if (s["title"], s["artist"]) not in existing_set]

        if not new_songs:
            return 0

        mongo_result = await self.collection.insert_many(new_songs)
        inserted_ids = mongo_result.inserted_ids

        texts = [
            f"{s.get('title')} {s.get('artist')} {s.get('genre')} {s.get('lyrics')}"
            for s in new_songs
        ]

        embeddings = generate_song_embeddings(texts)

        points = []

        for song, _id, vector in zip(new_songs, inserted_ids, embeddings):
            points.append(
                {
                    "id": str(_id),
                    "vector": vector,
                    "payload": {
                        "genre": song.get("genre"),
                        "artist": song.get("artist"),
                    },
                }
            )

        for i in range(0, len(points), QDRANT_BATCH_SIZE):
            self.qdrant.upsert(
                collection_name=self.qdrant_collection,
                points=points[i : i + QDRANT_BATCH_SIZE],
            )

        return len(points)
