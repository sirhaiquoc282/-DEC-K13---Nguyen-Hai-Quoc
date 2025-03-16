import logging


class Logger:
    def __init__(self, name, log_file, log_level):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler = logging.FileHandler(log_file)
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
