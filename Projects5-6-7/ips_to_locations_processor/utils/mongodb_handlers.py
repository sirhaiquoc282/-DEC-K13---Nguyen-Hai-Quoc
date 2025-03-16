from pymongo.errors import BulkWriteError
from configs.configs import DATABASE_NAME, COLLECTION_NAME


class MongoHandler:
    def __init__(
        self,
        logger,
        client,
        database_name=DATABASE_NAME,
        collection_name=COLLECTION_NAME,
    ):
        self.client = client
        self.database_name = database_name
        self.collection_name = collection_name
        self.logger = logger

    def get_unique_ips(self):
        try:
            pipeline = [
                {"$group": {"_id": "$ip"}},
                {"$project": {"_id": 0, "ip": "$_id"}},
            ]
            cursor = self.client[self.database_name][self.collection_name].aggregate(
                pipeline, allowDiskUse=True
            )
            uniq_ips = list(doc["ip"] for doc in cursor)
            self.logger.info(
                f"Got {len(uniq_ips)} unique ips from collection {self.collection_name} successfully."
            )
            return uniq_ips
        except Exception as e:
            self.logger.error(
                f"Failed to get unique ips from collection {self.collection_name}: {e}"
            )
            raise

    def insert_locations(self, locations_info):
        try:
            if not locations_info:
                self.logger.warning("Empty batch, skipping insert.")
                return

            self.client[self.database_name]["locations"].insert_many(locations_info)
            self.logger.info(
                f"Inserted {len(locations_info)} locations into MongoDB successfully"
            )
            return True

        except BulkWriteError as e:
            self.logger.error(
                f"BulkWriteError - Failed to insert locations: {e.details}"
            )
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error when inserting locations: {e}")
            raise
