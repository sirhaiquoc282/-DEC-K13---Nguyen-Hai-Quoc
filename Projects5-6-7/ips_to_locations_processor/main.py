import argparse
from utils.ip_processor import IPProcessor
from pymongo import MongoClient
from configs.configs import (
    MONGO_URI,
    DATABASE_NAME,
    COLLECTION_NAME,
    UNIQUE_IPS_FILE_LOCATION,
    APP_LOG,
    BATCH_SIZE,
    PROCESSED_DATA_LOG,
)
from utils.logger import Logger


def main() -> None:
    logger = Logger()

    parser = argparse.ArgumentParser(
        description="Convert unique IPs get from MongoDB and save to new collection"
    )

    parser.add_argument(
        "--mongo_uri", type=str, default=MONGO_URI, help="MongoDB connection URI"
    )
    parser.add_argument(
        "--database_name", type=str, default=DATABASE_NAME, help="Database name"
    )
    parser.add_argument(
        "--collection_name", type=str, default=COLLECTION_NAME, help="Collection name"
    )
    parser.add_argument(
        "--unique_ips_file",
        type=str,
        default=UNIQUE_IPS_FILE_LOCATION,
        help="Unique IPs file",
    )
    parser.add_argument(
        "--processed_data_log",
        type=str,
        default=PROCESSED_DATA_LOG,
        help="Processed data log",
    )
    parser.add_argument("--app_log", type=str, default=APP_LOG, help="app.log")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument(
        "--last_batch_num", type=int, default=0, help="Last batch number"
    )
    parser.add_argument("--first_num", type=int, default=0, help="First number")
    parser.add_argument("--last_num", type=int, default=0, help="Last number")

    args = parser.parse_args()

    try:
        client = MongoClient(args.mongo_uri)
        logger.info("Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

    try:
        processor = IPProcessor(logger, args, client)
        processor.process_ips()
        logger.info("Processing complete!")
    except Exception as e:
        logger.error(f"An error occurred during IP processing: {e}")
        raise


if __name__ == "__main__":
    main()
