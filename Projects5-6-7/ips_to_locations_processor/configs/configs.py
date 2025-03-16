import os
import logging


MONGO_URI = "mongodb://admin:Nguyenhaiquoc13571790@34.87.14.24:27017/?authSource=admin"
DATABASE_NAME = "countly"
COLLECTION_NAME = "summary"

UNIQUE_IPS_FILE_LOCATION = "data/ips.txt"
PROCESSED_DATA_LOG = "data/log.txt"
LOG_DIR = "logs"
APP_LOG = os.path.join(LOG_DIR, "app.log")

IP2LOCATION_FILE = "data/IP-COUNTRY-REGION-CITY.BIN"

BATCH_SIZE = 1000000

LOG_LEVEL = logging.INFO
