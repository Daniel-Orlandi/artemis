import multiprocessing
import numpy as np
import pandas

from utils import data_logger
from itertools import chain, starmap


class Extractor:
    def __init__(self, data_dict: dict) -> None:
        self.data_dict = data_dict
        self.logger = data_logger.Logger().set_logger(__name__)

    def get_data(self):
        return self.data_dict

    @staticmethod
    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in json file"""
        # Unpack one level only!!!

        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                temp1 = parent_key + '_' + key
                yield temp1, value
        elif isinstance(parent_value, list):
            i = 0
            for value in parent_value:
                temp2 = parent_key + '_'+str(i)
                i += 1
                yield temp2, value
        else:
            yield parent_key, parent_value

    def flatten_dict(self) -> pandas.DataFrame:
        while True:
            # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
            self.data_dict = dict(chain.from_iterable(
                starmap(self.unpack, self.data_dict.items())))

            # Terminate condition: not any value in the json file is dictionary or list
            if (not any(isinstance(value, dict) for value in self.data_dict.values()) and
                    not any(isinstance(value, list) for value in self.data_dict.values())):
                break
