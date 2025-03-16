import argparse
import logging
from configs.settings import (
    MONGO_URI,
    DB_COLLECTIONS,
    FLATFILE_PATHS,
    LOG_FILE,
    LOG_LEVEL,
    LOG_NAME,
    BATCH_SIZE,
    BUCKET_NAME,
    CREDENTIAL_PATH,
    BASE_PATH,
    log_levels,
)
from utils.mongo_utils import MongoManager
from utils.gcs_utils import GCSManager
from utils.logger import Logger
from pipelines.data_pipelines import export_mongodb_collections, upload_flatfiles


def parse_collections(raw_collections):
    return [tuple(pair.split(":")) for pair in raw_collections if ":" in pair]


def main():
    parser = argparse.ArgumentParser(description="Data Pipeline")
    parser.add_argument(
        "--mongo_uri", type=str, default=MONGO_URI, help="MongoDB connection URI"
    )
    parser.add_argument(
        "--db_collections",
        type=str,
        nargs="+",
        default=DB_COLLECTIONS,
        help="List of 'db:collection' pairs to export from MongoDB",
    )
    parser.add_argument(
        "--flatfile_paths",
        type=str,
        nargs="+",
        default=FLATFILE_PATHS,
        help="Paths to local CSV files for upload",
    )
    parser.add_argument(
        "--bucket_name", type=str, default=BUCKET_NAME, help="GCS bucket name"
    )
    parser.add_argument(
        "--base_path",
        type=str,
        default=BASE_PATH,
        help="Base path in GCS for uploaded data",
    )
    parser.add_argument(
        "--log_file", type=str, default=LOG_FILE, help="Path to log file"
    )
    parser.add_argument(
        "--log_level", type=str, default=LOG_LEVEL, help="Logging level"
    )
    parser.add_argument("--log_name", type=str, default=LOG_NAME, help="Logger name")
    parser.add_argument(
        "--batch_size", type=int, default=BATCH_SIZE, help="Size of each chunk"
    )
    parser.add_argument(
        "--credential_path",
        type=str,
        default=CREDENTIAL_PATH,
        help="Path to credential file",
    )
    args = parser.parse_args()

    try:
        logger = Logger(
            name=args.log_name,
            log_file=args.log_file,
            log_level=log_levels.get(args.log_level.lower(), logging.INFO),
        )
        mongo_manager = MongoManager(logger, args.mongo_uri)
        gcs_manager = GCSManager(logger, args.credential_path)

        collections = parse_collections(args.db_collections)
        export_mongodb_collections(
            logger,
            mongo_manager,
            gcs_manager,
            args.bucket_name,
            collections,
            args.base_path,
            args.batch_size,
        )
        upload_flatfiles(
            logger,
            gcs_manager,
            args.bucket_name,
            args.flatfile_paths,
            args.base_path,
        )

    except Exception as e:
        logger.error(e)
        raise
    finally:
        if "mongo_manager" in locals():
            mongo_manager.close()


if __name__ == "__main__":
    main()
