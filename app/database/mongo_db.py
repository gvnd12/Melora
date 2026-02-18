import logging
from time import time

from pymongo import AsyncMongoClient

from app.core.config import settings
from app.tools.constants import ResponseMessage
from app.tools.utils import generate_uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mongo_client = AsyncMongoClient(host=settings.MONGO_HOST_URL)
now = time()


class MongoDB:
    collection_name: str = None

    def __init__(self):
        self.database = mongo_client[settings.MONGO_DATABASE]
        self.collection = self.database[self.collection_name]

    async def prepare_metadata(self, document: dict):
        return {
            "_id": generate_uuid(),
            **document,
            "is_deleted": False,
            "created_at": int(now),
            "updated_at": None,
        }

    async def write_entry(self, document: dict):

        data = await self.prepare_metadata(document)
        result = await self.collection.insert_one(document=data)

        logger.info(msg=f"Database entry of {data.get('_id')} successful.")
        return result, ResponseMessage.CREATE_SUCCESS.value

    async def read_entry(
        self, filter_domain: dict | None = None, projection: dict | None = None
    ) -> dict:

        records = await self.collection.find(
            filter=filter_domain or {}, projection=projection or {}
        ).to_list()

        return {"message": ResponseMessage.GET_SUCCESS.value, "data": records}
