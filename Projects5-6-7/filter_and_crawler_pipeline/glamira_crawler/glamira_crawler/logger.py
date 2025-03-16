import logging
from glamira_crawler.settings import LOG_FILE, LOG_LEVEL


class Logger:
    def __init__(self, log_file=LOG_FILE, log_level=LOG_LEVEL):
        self.log_file = log_file
        self.log_level = log_level
        self.logger = self.get_logger()

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(self.log_level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
