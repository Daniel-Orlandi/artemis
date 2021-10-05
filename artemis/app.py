import datetime
import asyncio
import time
import pandas
from matplotlib.cbook import flatten

from artemis.core import response_handler, http_engine 
from artemis.core.data_extractor import Extractor
from artemis.models.cptec import CptecApiSuite
from artemis.models.inmet import InmetApiSuite
from artemis.models.metar import OnsMetarApiSuite
from artemis.models.location_model import Location
from artemis.core.sheet_engine import WorkBook
from artemis.utils import data_logger, check_d_type, read_json

class Carga:
  def __init__(self, date_begin:str,
               date_end:str,
               location_file_list:list,
               input_excel_file_list:list,
               output_excel_file_list:list,
               obs_host_list:list,
               cloud_cover_wcond_list:list,
               precipitation_wcond_list:list,
               period_wcond_list:list,
               fcast_host_list:list ) -> None:

      self.date_begin = date_begin
      self.date_end = date_end
      self.location_file_list = location_file_list
      self.input_excel_file_list = input_excel_file_list
      self.output_excel_file_list = output_excel_file_list
      self.obs_host_list = obs_host_list
      self.cloud_cover_wcond_list = cloud_cover_wcond_list
      self.precipitation_wcond_list = precipitation_wcond_list
      self.period_wcond_list = period_wcond_list
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


  @staticmethod
  def add_combo(workbook, wcond_list: list, combo_position_in_table_list:list, combo_position_in_table:str, dropdown_position) -> None:      
      workbook.set_cell(wcond_list, combo_position_in_table_list)
      data_val = workbook.add_drop_down(position=combo_position_in_table)
      data_val.add(workbook.get_active_table[dropdown_position])
  

  def write_data_to_table(self, workbook)->None:
        try:
            for location in self.__location_list:
                pos_in_table_list = list(location.data.keys())
                data_list = list(location.data.values())
                workbook.set_cell(data_list, pos_in_table_list)
                row = str(location.row)
                #adicona os combos necessários nas posições
                [self.add_combo(workbook,
                                self.cloud_cover_wcond_list,
                                combo_position_in_table_list = [f'C{str(pos)}' for pos in range(30, 30 + len(self.cloud_cover_wcond_list))] ,
                                combo_position_in_table="=$C$30:$C$44",
                                dropdown_position=pos_in_loc+row) for pos_in_loc in location.cloud_cover_w_cond]                 

                [self.add_combo(workbook,
                                self.precipitation_wcond_list,
                                combo_position_in_table_list = [f'D{str(pos)}' for pos in range(30, 30 + len(self.precipitation_wcond_list))],
                                combo_position_in_table="=$D$30:$D$44",
                                dropdown_position=pos_in_loc+row) for pos_in_loc in location.precip_w_cond]

                [self.add_combo(workbook,
                                self.period_wcond_list,
                                combo_position_in_table_list = [f'E{str(pos)}' for pos in range(30, 30 + len(self.period_wcond_list))] ,
                                combo_position_in_table="=$E$30:$E$44",
                                dropdown_position=pos_in_loc+row) for pos_in_loc in location.period_w_cond]
        
        except Exception as general_error:
            self.logger.error(f'Error: {general_error}')
                 

  def set_locations(self, file) -> None:
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
        
    except Exception as general_error:
      self.logger.error(f'General error: {general_error}')       


  def make_forecast(self, host:str) -> dict:
    try:
      if (host == "cptec"):
        cptec_location_list = []
        [cptec_location_list.append(location.cptec_id) for location in self.__location_list]
        cptec_location_list = list(flatten(cptec_location_list))
        model = CptecApiSuite(cptec_location_list)
        model.get_forecast_by_date_delta(num_days='4days')
        model.make_request("async")        
      
      else:
        raise Exception('Not yet implemented.')

    except Exception as general_error:
      self.logger.error(f'General error: {general_error}') 
          
    else:
      return model.get_data_dict()


  def make_observation(self, host:str) -> dict:
    try:
      if (host == "inmet"):
        inmet_location_list = []
        [inmet_location_list.append(location.ws_id) for location in self.__location_list]
        inmet_location_list = list(flatten(inmet_location_list))
        model = InmetApiSuite(inmet_location_list)
        url = model.base_url + "/estacao/{}/{}/{}"
        

      elif (host == "ons-metar"):
        ons_metar_location_list = []
        [ons_metar_location_list.append(location.icao_id) for location in self.__location_list]
        model = OnsMetarApiSuite(ons_metar_location_list)
        url = model.base_url +"dataInicioPeriodo={}&dataFimPeriodo={}&estacaoId={}&mnemonico=DRYT&modelo=METAR&pagina=1&itensPorPagina=500"

      else:
          raise Exception('Not yet implemented.') 
      
      model.set_request_dict_by_date_range(date_begin=self.date_begin, date_end=self.date_end, url=url)
      model.make_request("async")           

    except Exception as general_error:
      self.logger.error(f'General error: {general_error}')
          
    else:
      return model.get_data_dict() 

  def write_to_excel(self, input_filename, save_filename) -> None:
    try:
      self.logger.info('Beginning data pre-processing')
      my_extractor = Extractor(self.__data_dict, self.__location_list)
      my_extractor.set_carga()
      self.logger.info('Done.')
      
      self.logger.info('Writing data to excel file.')      
      my_workbook = WorkBook(location_list=self.__location_list, filename=input_filename)
      my_workbook.load_sheet(keep_vba=True)
      my_workbook.set_active_table("Tabela")
      my_workbook.set_date_cell(self.date_end, "A1")      
      self.write_data_to_table(my_workbook) 
      my_workbook.save_sheet(my_workbook.get_workbook, save_filename + self.date_end +'.xlsm')

    except Exception as general_error:
      self.logger.error(f'General error: {general_error}') 
      
    
  def multi_run(self, data_list:list, func) -> list:
     self.logger.info("Multi-run method called. Running")

     try:      
       result_list = [func(item) for item in data_list]  
       return result_list
    
     except Exception as general_error:
       self.logger.error(f'General error: {general_error}')
       







  

      



  
  
