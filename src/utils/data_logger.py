import logging
import sys
from logging.handlers import TimedRotatingFileHandler


class Logger:
    """
    docstring
    """

    def __init__(self, filename: str, level, filemode: str, log_format: str, datefmt: str) -> None:
        self.filename = filename
        self.level = level
        self.filemode = filemode
        self.log_format = log_format
        self.datefmt = datefmt

        logging.basicConfig(filename= self.filename,
                            level = self.level,
                            filemeode =self.filemode,
                            format = self.log_format,
                            datefmt = self.datefmt)

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.log_format)
        return console_handler

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.filename, when='midnight')
        file_handler.setFormatter(self.log_format)
        return file_handler

    def set_logger(self, logger_name) -> object:
        logger = logging.getLogger(logger_name)
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger

