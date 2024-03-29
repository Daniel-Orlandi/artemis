from artemis import utils
import sys
import pathlib
from logging.handlers import TimedRotatingFileHandler
import logging.config

class Logger:
    """ 
    Logger class 
    ...

    Attributes
    ----------
    logger_name:str
        logger choosen name.

    filename: str = None
        if not none, log file name, where the logs will be saved.
        else, filename will be log_file.log at project root.

    log_format: str = None
        if not none, change log formating.
        else, use standart log formating : 2020-12-23 14:23:05
    Methods
    -------
    get_logger(self):
        get logger.

    """

    def __init__(self, logger_name:str, filename:str = None, log_format: str = None):
        self.logger_name = logger_name
        self.logger = None        
        
        if (isinstance(filename, str)):
            self.filename = filename

        else:
            self.filename = "data/logs/log_file.log"
            if(utils.check_exists(self.filename) == False):
                path = os.path.dirname(self.filename)
                path = pathlib.Path(path)
                path.parent.mkdir(parents=True, exist_ok=True) 
                open("log_file.log","x")

            self.filename = "data/logs/log_file.log"

        if (isinstance(log_format, str)):
            self.log_format = logging.Formatter(log_format)

        else:
            pass
       
        logging.config.fileConfig("/home/mdata/daniel/artemis/resources/config_files/logger_config.conf")
        self.logger = logging.getLogger(self.logger_name)

    def get_logger(self):    
        return self.logger
    

        
