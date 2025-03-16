import logging

MONGO_URI = "mongodb://admin:Nguyenhaiquoc13571790@34.87.14.24:27017/?authSource=admin"

DB_COLLECTIONS = ["countly:summary", "countly:locations"]
FLATFILE_PATHS = []

LOG_FILE = "logs/app.log"
LOG_LEVEL = "info"
LOG_NAME = "extractor"

BUCKET_NAME = "raw-glamira"
CREDENTIAL_PATH = "D:\Personal\Projects\lv1_final_project\data_export_process\woven-plane-448115-r4-301e5b4d4c61.json"
BASE_PATH = "glamira_v1"
BATCH_SIZE = 100000

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
