class CptecApiSuite:
    def __init__(self, id_locale: list = None):
        self.__base_url = "http://servicos.cptec.inpe.br/XML"
        self.id_locale = id_locale
    
    def __test_if_id_locale(self) -> bool:
        if (self.id_locale == None):
            return False
        
        else:
            True

    def get_4days_forecast(self) -> dict:
        if (self.__test_if_id_locale == False):
            raise Exception ('To use this method, a id_locale should be provided.')

        forecast_url = "cidade/{}/previsao.xml"

        url_dict = {}

        for city_id in self.id_locale:
            url = self.__base_url + forecast_url.format(city_id)
            url_dict[city_id] = url

        return url_dict

    def get_7days_forecast(self) -> dict:
        if (self.__test_if_id_locale == False):
            raise Exception ('To use this method, a id_locale should be provided.')

        forecast_url = "/cidade/7dias/{}/previsao.xml"

        url_dict = {}

        for city_id in self.id_locale:
            url = self.__base_url + forecast_url.format(city_id)
            url_dict[city_id] = url

        return url_dict

    def get_current_weather_condition_capitals(self)->dict:
        forecast_url = "/capitais/condicoesAtuais.xml"        
        url_dict = {}
        url = self.__base_url + forecast_url
        url_dict['current_weather_cond_capitals'] = url
        return url_dict

    # def get_current_weather_condition_stations(self)->dict:
