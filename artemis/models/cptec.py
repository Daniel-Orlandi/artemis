from urllib.parse import urlparse

from utils import data_logger


class CptecApiSuite:
    def __init__(self, id_locale: list = None):
        self.__base_url = "http://servicos.cptec.inpe.br/XML"
        self.hostname = urlparse(self.__base_url).hostname
        self.id_locale = id_locale
        self.logger = data_logger.Logger().set_logger(__name__)

    def get_forecast(self, num_days: str) -> dict:
        try:
            if (not isinstance(self.id_locale, list)):
                raise Exception(
                        'To use this method, a id_locale should be provided.')

            if (isinstance(num_days, str) and num_days == '4days'):
                forecast_url = "/cidade/{}/previsao.xml"

            elif (isinstance(num_days, str) and num_days == '7days'):
                forecast_url = "/cidade/7dias/{}/previsao.xml"

            else:
                raise Exception('Only 4 or 7 days forecast is available.')
                
            url_dict = {}

            for city_id in self.id_locale:
                url = self.__base_url + forecast_url.format(city_id)
                url_dict[str(city_id)] = url
                self.logger.info(url)
                
            return {self.hostname:url_dict}
            
        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error
        
    def get_current_weather_condition_capitals(self) -> dict:
        forecast_url = "/capitais/condicoesAtuais.xml"
        url_dict = {}
        url = self.__base_url + forecast_url
        url_dict['current_weather_cond_capitals'] = url
        return {self.hostname:url_dict}
