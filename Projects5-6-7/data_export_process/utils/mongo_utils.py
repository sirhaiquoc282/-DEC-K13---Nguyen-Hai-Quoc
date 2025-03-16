from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError
from bson import ObjectId


class MongoManager:
    def __init__(self, logger, connection_uri):
        self._client = MongoClient(connection_uri)
        self.logger = logger
        self._verify_connection()

    def _verify_connection(self):
        try:
            self._client.admin.command("ping")
            self.logger.info("Connected to MongoDB successfully")
        except PyMongoError as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_collection_cursor(self, db_name, collection_name, last_id=None):
        try:
            collection = self._client[db_name][collection_name]
            query = {"_id": {"$gt": ObjectId(last_id)}} if last_id else {}
            return collection.find(query).sort("_id", ASCENDING).batch_size(1000)
        except PyMongoError as e:
            self.logger.error(f"Failed to query data: {e}")
            raise

    def close(self):
        self._client.close()
