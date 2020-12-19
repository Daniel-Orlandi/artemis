import logging
import sys
from logging.handlers import TimedRotatingFileHandler


class Logger:
    """
    docstring
    """

    def __init__(self, filename: str, log_format: str) -> None:
        self.filename = filename               
        self.log_format = logging.Formatter(log_format)      
        
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
        logger.setLevel(logging.DEBUG)        
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger

