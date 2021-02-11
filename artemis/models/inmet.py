from utils import check_date_format
from .base import BaseModel

class InmetApiSuite(BaseModel):
  BaseModel.base_url = "https://apitempo.inmet.gov.br" 
