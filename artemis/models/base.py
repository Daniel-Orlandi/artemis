import datetime
from utils import data_logger, check_date_format

class BaseModel:
    def __init__(self, id_locale_list: list = None):                        
        self.id_locale_list = id_locale_list
        self.logger = data_logger.Logger().set_logger(__name__)

    def check_if_id_locale(self):
        if (not isinstance(self.id_locale_list, list)):
            raise Exception(
                'To use this method, a id_locales should be provided.')
    

    def set_request_dict_by_date_range (self, url, date_begin, date_end) -> dict:

        try:
            self.check_if_id_locale()
            check_date_format(date_begin, '%Y-%m-%d')
            check_date_format(date_end, '%Y-%m-%d') 

            url_dict = {}            
            for city_id in self.id_locale_list:
                request_url = url.format(date_begin, date_end, city_id)
                url_dict[str(city_id)] = request_url.format(date_begin, date_end, city_id)
                self.logger.info(request_url)

            return url_dict

        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error  
      

    
