import logging.config
import sys
from logging.handlers import TimedRotatingFileHandler


class Logger:
    """ 
    Logger class 
    ...

    Attributes
    ----------
    filename: str = None
        if not none, log file name, where the logs will be saved.
        else, filename will be log_file.log at project root.

    log_format: str = None
        if not none, change log formating.
        else, use standart log formating : 2020-12-23 14:23:05,845 — api — INFO — get_data:72 — async mode selected.

    Methods
    -------
    get_console_handler(self):
        get handles for logger.

    get_file_handler(self):
        get file handles for logger.

    set_logger(self, logger_name) -> object:
        set logger configuration.

    TODO
    ----
    use config through log file.
    """

    def __init__(self, filename: str = None, log_format: str = None):
        if (isinstance(filename, str)):
            self.filename = filename
        else:
            self.filename = "logs/log_file.log"

        if (isinstance(log_format, str)):
            self.log_format = logging.Formatter(log_format)
        else:
            self.log_format = logging.Formatter(
                "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")        

    def __get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.log_format)
        return console_handler

    def __get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.filename, when='midnight')
        file_handler.setFormatter(self.log_format)
        return file_handler

    def set_logger(self, logger_name) -> object:
        """
        Method that sets the logger with all configurations needed.

        Parameters
        ----------
        logger_name: str
            Logger name  
        """

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.__get_console_handler())
        logger.addHandler(self.__get_file_handler())
        logger.propagate = True
        return logger
