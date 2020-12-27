import multiprocessing
import numpy as np
import pandas

from utils import data_logger

class Extractor:
    def __init__(self, data_dict: dict) -> None:
        self.data_dict = data_dict
        self.logger = data_logger.Logger().set_logger(__name__)
    
    @staticmethod       
    def data_to_dataframe(data: dict) -> pandas.DataFrame:
                
        pass
        
        