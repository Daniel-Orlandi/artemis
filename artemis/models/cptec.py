from .base import BaseModel


class CptecApiSuite(BaseModel):     
    BaseModel.base_url = "http://servicos.cptec.inpe.br/XML"
    BaseModel.forecast_url = "/cidade/"

    def get_forecast_by_date_delta(self, num_days: str) -> dict:
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

            return url_dict

        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error

    def get_current_weather_condition_capitals(self) -> dict:
        final_url = "/capitais/condicoesAtuais.xml"
        url_dict = {}
        url = self.base_url + final_url
        url_dict['current_weather_cond_capitals'] = url
        return url_dict
