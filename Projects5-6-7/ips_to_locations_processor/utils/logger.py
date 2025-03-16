import logging
import os
from configs.configs import LOG_LEVEL, APP_LOG


class Logger:
    def __init__(self, log_file=APP_LOG, log_level=LOG_LEVEL):
        self.log_file = log_file
        self.log_level = log_level
        self.logger = logging.getLogger("app_logger")
        self.logger_init()

    def logger_init(self):
        log_dir = os.path.dirname(self.log_file)
        os.makedirs(log_dir, exist_ok=True)
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

        self.logger.setLevel(self.log_level)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)
