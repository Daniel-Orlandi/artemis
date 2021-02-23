import datetime
import asyncio
from logging import root
import time
import pandas
from matplotlib.cbook import flatten

from artemis.core import response_handler, http_engine 
from artemis.core.data_extractor import Extractor
from artemis.models.cptec import CptecApiSuite
from artemis.models.inmet import InmetApiSuite
from artemis.models.location_model import Location
from artemis.core.sheet_engine import WorkBook
from artemis.utils import data_logger, check_d_type, read_json

class MainFactory:
  def __init__(self, date_begin:str,
               date_end:str,
               input_excel_file_list:list,
               output_excel_file_list:list,
               obs_host_list:list,
               fcast_host_list:list ) -> None:

      self.date_begin = date_begin
      self.date_end = date_end
      self.input_excel_file_list = input_excel_file_list
      self.output_excel_file_list = output_excel_file_list
      self.obs_host_list = obs_host_list
      self.fcast_host_list = fcast_host_list
      self.__location_list = None
      self.__data_dict = None
      self.logger = data_logger.Logger(logger_name=__name__).get_logger()
  
  def set_data_dict(self, data_dict:dict) -> None:
    self.__data_dict = data_dict
  
  @property
  def get_location_list(self) -> list:
    return self.__location_list

  @property
  def get_data_dict(self) -> dict:
    return self.__data_dict

  @staticmethod
  def read_location_file(location_json_dict:str, query:str = 'cities') -> list:
    location_list = []
    for city in location_json_dict[query]:
      my_location = Location()
      my_location.set_location(city)
      location_list.append(my_location)
    
    return location_list

  def set_locations(self, file):
    try:
      if isinstance(file, list):
        for item in file:
         item = read_json(item)
         location_list = self.read_location_file(item)
         self.__location_list = location_list

      elif isinstance(file, str):
        file = read_json(file)
        location_list = self.read_location_file(file)
        self.__location_list = location_list

      else:
        raise ValueError( f'{file} must be a list or a string containing paths/path to file.')

    except ValueError as value_error:
      self.logger.error(f'Value error: {value_error}')
      raise value_error 
        
    except Exception as general_error:
      self.logger.error(f'General error: {general_error}')
      raise general_error 
      
  def make_forecast(self, host:str) -> dict:
    try:
      if (host == "cptec"):
        cptec_location_list = []
        [cptec_location_list.append(location.cptec_id) for location in self.__location_list]
        cptec_location_list = list(flatten(cptec_location_list))
        model = CptecApiSuite(cptec_location_list)
        model.get_forecast_by_date_delta(num_days='4days')
        model.make_request("async")
        return model.get_data_dict()
      
      else:
        raise Exception('Not yet implemented.')

    except Exception as general_error:
      self.logger.error(f'General error: {general_error}') 
      raise general_error
        
  def make_observation(self, host:str) -> dict:
    try:
      if (host == "inmet"):
        inmet_location_list = []
        [inmet_location_list.append(location.ws_id) for location in self.__location_list]
        inmet_location_list = list(flatten(inmet_location_list))
        model = InmetApiSuite(inmet_location_list)
        url = model.base_url + "/estacao/{}/{}/{}"
        model.set_request_dict_by_date_range(date_begin=self.date_begin, date_end=self.date_end, url=url)
        model.make_request("async")
        return model.get_data_dict()

      else:
          raise Exception('Not yet implemented.')

    except Exception as general_error:
      self.logger.error(f'General error: {general_error}')
      raise general_error     
    
  def write_to_excel(self) -> None:
    try:
      self.logger.info('Beginning data pre-processing')
      my_extractor = Extractor(self.__data_dict, self.__location_list)
      my_extractor.set_carga()
      self.logger.info('Done.')
      
      self.logger.info('Writing data to excel file.')
      for input_file, save_file in list(zip(self.input_excel_file_list, self.output_excel_file_list)):
          my_workbook = WorkBook(location_list=self.__location_list, filename=input_file)
          my_workbook.load_sheet(keep_vba=True, data_only=False)
          my_workbook.set_active_table("Tabela")
          my_workbook.set_date_cell(self.date_end, "A1")
          my_workbook.write_data_to_table() 
          my_workbook.save_sheet(my_workbook.get_workbook, save_file + self.date_begin +'.xlsm')

    except Exception as general_error:
      self.logger.error(f'General error: {general_error}') 
      raise general_error
    
  def multi_run(self, data_list:list, func) -> list:
     self.logger.info("Multi-run method called. Running")

     try:      
       result_list = [func(item) for item in data_list]  
       return result_list
    
     except Exception as general_error:
       self.logger.error(f'General error: {general_error}')
       raise general_error







  

      



  
  
