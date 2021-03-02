from artemis.utils import check_date_format
from .base import BaseModelInterface

class InmetApiSuite(BaseModelInterface):
  def __init__(self, id_locale_list: list):
      super().__init__(id_locale_list=id_locale_list)     
      self.base_url = "https://apitempo.inmet.gov.br" 
      
