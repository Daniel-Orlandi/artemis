import datetime
import asyncio
from artemis.utils import check_date_format, check_d_type
from artemis.utils.data_logger import Logger
from artemis.core.http_engine import Request

class BaseModelInterface:
    def __init__(self, id_locale_list:list = None):                        
        self.id_locale_list = id_locale_list
        self.logger = Logger(logger_name=__name__).get_logger()
        self.data_dict = None
    
    def get_data_dict(self):
        return self.data_dict

    def check_if_id_locale(self):
        if (not isinstance(self.id_locale_list, list)):
            raise Exception('To use this method, a id_locales should be provided.')    

    def set_request_dict_by_date_range (self, url, date_begin, date_end) -> None:

        try:
            self.check_if_id_locale()
            check_date_format(date_begin, '%Y-%m-%d')
            check_date_format(date_end, '%Y-%m-%d') 

            url_dict = {}            
            for city_id in self.id_locale_list:
                request_url = url.format(date_begin, date_end, city_id)
                url_dict[str(city_id)] = request_url.format(date_begin, date_end, city_id)
                self.logger.info(request_url)

            self.data_dict=url_dict

        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error  

    def make_request(self, mode: str) -> None:
        try:
            check_d_type(mode, str)
            getter = Request(data_dict=self.data_dict)
            asyncio.run(getter.get(method=mode))
            self.__data_dict = getter.get_data_dict()
        
        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error 


    
