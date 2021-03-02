import asyncio
from artemis.models.base import BaseModelInterface
from artemis.models.location_model import Location
from artemis.utils import check_d_type

class CptecApiSuite(BaseModelInterface):
    def __init__(self, id_locale_list: list):
        super().__init__(id_locale_list=id_locale_list)     
        self.base_url = "http://servicos.cptec.inpe.br/XML"
        self.forecast_url = "/cidade/"
                
    def get_forecast_by_date_delta(self, num_days: str) -> None:
        try:
            self.check_if_id_locale()

            if (isinstance(num_days, str) and num_days == '4days'):
                final_url = self.forecast_url + "{}/previsao.xml"

            elif (isinstance(num_days, str) and num_days == '7days'):
                final_url = self.forecast_url + "7dias/{}/previsao.xml"

            else:
                raise Exception('Only 4 or 7 days forecast is available.')

            url_dict = {}
            for city_id in self.id_locale_list:
                url = self.base_url + final_url.format(city_id)
                url_dict[str(city_id)] = url
                self.logger.info(url)

            self.data_dict = url_dict

        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error

    def get_current_weather_condition_capitals(self) -> dict:
        final_url = "/capitais/condicoesAtuais.xml"
        url_dict = {}
        url = self.base_url + final_url
        url_dict['current_weather_cond_capitals'] = url
        return url_dict
    
    



