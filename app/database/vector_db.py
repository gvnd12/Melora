from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings

qdrant = QdrantClient(url=settings.QDRANT_URL)


def create_qdrant_collection():

    collection = settings.QDRANT_SONGS_COLLECTION

    is_collection_exists = qdrant.get_collection(collection_name=collection)

    if is_collection_exists:
        return

    qdrant.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
