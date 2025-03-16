from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    ServerSelectionTimeoutError,
    OperationFailure,
)
from glamira_crawler.logger import Logger
from glamira_crawler.settings import MONGO_URI, DB_NAME, COLLECTION_NAME


class MongoDB:
    def __init__(
        self, mongo_uri=MONGO_URI, db_name=DB_NAME, collection_name=COLLECTION_NAME
    ):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = self.connect()
        self.logger = Logger()

    def connect(self):
        try:
            client = MongoClient(self.mongo_uri)
            client.server_info()
            return client
        except (ConnectionFailure, ServerSelectionTimeoutError, OperationFailure) as e:
            self.logger.error(e)
            raise e

    def filter_data(self):
        try:
            client = self.client
            db = client[self.db_name]
            collection = db[self.collection_name]
            pipeline = [
                {
                    "$match": {
                        "collection": {
                            "$in": [
                                "view_product_detail",
                                "select_product_option",
                                "select_product_option_quality",
                            ]
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$product_id",
                        "current_url": {"$first": "$current_url"},
                    }
                },
                {"$project": {"_id": 0, "product_id": "$_id", "current_url": 1}},
            ]
            cursor = collection.aggregate(pipeline, allowDiskUse=True)
            return cursor
        except (ConnectionFailure, ServerSelectionTimeoutError, OperationFailure) as e:
            self.logger.error(e)
            raise e
