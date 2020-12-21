import logging
import sys
from logging.handlers import TimedRotatingFileHandler

class Logger:
    """
    docstring
    """
    
    def __init__(self, filename: str = None, log_format: str = None):
        if (isinstance(filename,str)):
            self.filename = filename        
        else:
            self.filename = "log_file.log"
            
        if (isinstance(log_format, str)):
            self.log_format = logging.Formatter(log_format)
        else:
            self.log_format = logging.Formatter(
                "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")

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
        logger.propagate = True
        return logger