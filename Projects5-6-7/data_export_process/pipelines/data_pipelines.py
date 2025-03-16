import json
from typing import List, Tuple
from pathlib import Path
from utils.type_converter import type_convertor


def export_mongodb_collections(
    logger,
    mongo_manager,
    gcs_manager,
    bucket_name,
    collections: List[Tuple[str, str]],
    base_path,
    batch_size,
):

    for db_name, collection_name in collections:
        checkpoint_path = f"{base_path}/{db_name}/{collection_name}/checkpoint.json"
        target_path = f"{base_path}/{db_name}/{collection_name}/{collection_name}"

        try:
            last_id, part_number = gcs_manager.load_checkpoint(
                bucket_name, checkpoint_path
            )
            cursor = mongo_manager.get_collection_cursor(
                db_name, collection_name, last_id
            )

            batch = []
            last_doc_id = None
            for doc in cursor:
                doc = type_convertor(doc)
                batch.append(json.dumps(doc, default=str))
                last_doc_id = doc["_id"]
                if len(batch) >= batch_size:
                    if gcs_manager.upload_batch(
                        bucket_name, target_path, batch, part_number
                    ):
                        part_number += 1
                        gcs_manager.save_checkpoint(
                            bucket_name, checkpoint_path, last_doc_id, part_number
                        )
                        batch = []

            if batch:
                if gcs_manager.upload_batch(
                    bucket_name, target_path, batch, part_number
                ):
                    gcs_manager.save_checkpoint(
                        bucket_name, checkpoint_path, last_doc_id, part_number + 1
                    )

        except Exception as e:
            logger.error(f"Failure to export for {db_name}.{collection_name}: {e}")
            continue


def upload_flatfiles(
    logger, gcs_manager, bucket_name, file_paths: List[str], base_path
):

    for file_path in file_paths:
        try:
            target_path = f"{bucket_name}/{base_path}/flatfiles/{Path(file_path).name}"
            with open(file_path, "rb") as local_file:
                with gcs_manager._fs.open(target_path, "wb") as gcs_file:
                    gcs_file.write(local_file.read())
            logger.info(f"Uploaded file {file_path} successfully")
        except Exception as e:
            logger.error(f"Failure to upload {file_path}: {e}")
