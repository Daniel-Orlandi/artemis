from utils import data_logger

class InmetApiSuite:
  def __init__(self, id_locale: list = None):
    self.__base_url = "https://apitempo.inmet.gov.br/estacao"
    self.id_locale = id_locale
    self.logger = data_logger.Logger().set_logger(__name__)

  
  def get_forecast(self, num_days: str) -> dict:
    

  def get_observation(self, num_days: str) -> dict:
