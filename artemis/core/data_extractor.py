import numpy as np
from openpyxl.descriptors.base import Bool
import pandas
import unidecode
import datetime

from artemis.utils import check_d_type
from artemis.utils.data_logger import Logger

class Extractor:
    def __init__(self, data_dict: dict, location_list: list) -> None:
        self.__data_dict = data_dict
        self.__data_frame = pandas.DataFrame
        self.__location_list = location_list
        self.logger = Logger(logger_name=__name__).get_logger()

    @property
    def get_data_dict(self):
        #Returns data contained in __data_dict       
        return self.__data_dict

    @property
    def get_dataframe(self):
        #Returns data contained in __data_frame
        return self.__data_frame
    
    @property
    def get_location_list(self):
        #Returns data contained in __location_list
        return self.__location_list
        
    def write_list(self, data_list, data, func, item_filter:Bool = None):
        for idx, item in enumerate(data_list):
            if (item_filter is not None):
                try:
                    if(item_filter == True):
                        func(item, data[idx])
                    
                    else:
                        pass
                except:
                    self.logger.info(f'No data found!')
                    func(item,str("nan"))

            elif (item_filter is None):
                try:
                    func(item,data[idx])
                    print(item, data)
            
                except:
                    self.logger.info(f'No data found!')
                    func(item,str("nan"))
            else:
                raise Exception(f'A error {Exception.with_traceback()} ocurred.')
            
            
    @staticmethod
    def get_temp(dataframe: pandas.DataFrame, mode: str) -> pandas.DataFrame:
        """
         method responsible get a dataframe configured from set_site_data method, and get min temp
         max temp, and site id/name. Dataframe columns should be:
         ['DATA','TEMP_MAX', 'TEMP_MIN', 'CD_ESTACAO', 'CIDADE']

        Parameters
        ----------
        dtaframe: pandas.Dataframe
            dataframe containing temperature data to be extracted.
        
        mode: str
            Type of temp to be selected. Accepts TEMP_MAX or TEMP_MIN
            
        Returns
        ----------
        pandas.Dataframe
            dataframe containing selected data for given location.

        Raises
        ----------
        TypeError
            "mode must be a str and equal to TEMP_MAX or TEMP_MIN."    

        """  
        check_d_type(dataframe, pandas.DataFrame) 
        check_d_type(mode, str)   
        temp_data_frame = dataframe

        if (isinstance(mode, str) and mode == 'TEMP_MAX'):            
            temp_data_frame = temp_data_frame.drop(columns=['TEMP_MIN'])
            result = pandas.DataFrame()

            for day in temp_data_frame['DATA'].dt.day.unique():
                data_frame_no_other_temp = temp_data_frame[temp_data_frame['DATA'].dt.day == day]

                for city in data_frame_no_other_temp['CIDADE'].unique():  
                    temp_data = data_frame_no_other_temp[data_frame_no_other_temp['CIDADE'] == city]
                    temp_data = temp_data.loc[temp_data[mode] == temp_data[mode].max()]
                    temp_data = temp_data.rename(columns={'CD_ESTACAO':'CD_ESTACAO_max'})
                    result = pandas.concat([temp_data, result])

        elif (isinstance(mode, str) and mode == 'TEMP_MIN'):
            temp_data_frame = dataframe.drop(columns=['TEMP_MAX'])
            result = pandas.DataFrame()

            for day in temp_data_frame['DATA'].dt.day.unique():
                data_frame_no_other_temp = temp_data_frame[temp_data_frame['DATA'].dt.day == day]

                for city in data_frame_no_other_temp['CIDADE'].unique():  
                    temp_data = data_frame_no_other_temp[data_frame_no_other_temp['CIDADE'] == city]
                    temp_data = temp_data.loc[temp_data[mode] == temp_data[mode].min()]
                    temp_data = temp_data.rename(columns={'CD_ESTACAO':'CD_ESTACAO_min'})                                          
                    result = pandas.concat([temp_data, result])

        else:
            raise TypeError("mode must be a str and equal to TEMP_MAX or TEMP_MIN.")

        return result    
    
    def set_site(self, data_dict: dict) -> pandas.DataFrame:
        """
         method responsible for identify the given host and location(weather station, etc), 
         and set data retrieved acordingly. Dictionary received in this method are expected to be
         a implemented host, and have temp_min, max, date, and site name info.

        Parameters
        ----------
        data_dict: dict 
            Dict containing location(site) data to be set

        Returns
        ----------
        pandas.Dataframe
            dataframe containing data for given site.

        Raises
        ----------
        ValueError
            'host not recognized, you need to add it to the aplication.
             Contact development.!' 

        Exception
            catches any other error.

        """
        try:
            check_d_type(data_dict, dict)
            self.logger.info('Seting data.')
            host = data_dict['host']
            data = data_dict['data']

            if (host == 'servicos.cptec.inpe.br'):
                self.logger.info(f'host = CPTEC.')

                base = pandas.DataFrame.from_dict(data, orient='index')

                data = pandas.DataFrame(base['previsao'][0])
                data['cidade'] = base['nome']['cidade']
                data = data.rename(columns={'dia': 'DATA',
                                            'tempo': 'TEMPO',
                                            'maxima': 'TEMP_MAX',
                                            'minima': 'TEMP_MIN',
                                            'cidade': 'CIDADE'})

                data = data[['DATA', 'TEMP_MAX','TEMP_MIN', 'TEMPO', 'CIDADE']]                

            elif(host == 'apitempo.inmet.gov.br'):
                self.logger.info(f'host = INMET.')

                data = pandas.DataFrame(data)
                data = data.rename(columns={'DC_NOME': 'CIDADE',
                                            'DT_MEDICAO': 'DATA',
                                            'TEM_MAX':'TEMP_MAX',
                                            'TEM_MIN':'TEMP_MIN'})
                
                data = data[['DATA','TEMP_MAX', 'TEMP_MIN', 'CD_ESTACAO', 'CIDADE']]
                
            else:
                raise ValueError(
                    'host not recognized, you need to add it to the aplication. Contact development!')

            data['DATA'] =   data['DATA'].apply(lambda x: pandas.to_datetime(str(x), format='%Y-%m-%d'))
            data['CIDADE'] = data['CIDADE'].apply(lambda x: str(unidecode.unidecode(x)).upper())            
            return data

        except ValueError as value_error:
            self.logger.error(f'Value Error: {value_error}')
            
        except Exception as general_error:
            self.logger.error(f'Ops another error ocurred: {general_error}')
            

    def set_locations(self) -> None:        
        self.logger.info('concatenating all results in data_dict.')
        result = pandas.DataFrame()

        # aplica set_data linha a linha, pq set data foi pensado para funcionar por cidade
        for key, value in self.__data_dict.items():            
            df = self.set_site(value)
            self.logger.info('Location:{}'.format(df['CIDADE']))
            result = pandas.concat([result, df])            

        result[['TEMP_MAX', 'TEMP_MIN']] = result[['TEMP_MAX', 'TEMP_MIN']].apply(pandas.to_numeric)

        
        temp_min = self.get_temp(result, 'TEMP_MIN')
        self.logger.info('Done getting min.')
        
        temp_max = self.get_temp(result, 'TEMP_MAX')
        self.logger.info('Done getting max.')
        
        result = pandas.merge(temp_min, temp_max, how='outer')
        result = result.rename(columns={"DATA_x": "DATA"})
        result.index = result['DATA']
        result.drop(columns={'DATA'})
        result.sort_index(inplace=True)
        result = result[['CIDADE', 'TEMP_MAX', "CD_ESTACAO_max", 'TEMP_MIN', "CD_ESTACAO_min"]]
        self.__data_frame = result.drop_duplicates()
        
        for location in self.__location_list:
            data = self.__data_frame[self.__data_frame['CIDADE'] == location.name]            
            self.write_list(location.fcast_min_temp, data['TEMP_MIN'], location.store_data, item_filter=True if(datetime.datetime.today() == data.index and datetime.datetime.today().hour <= 12) else False)
            self.write_list(location.obs_min_temp, data['TEMP_MIN'], location.store_data, item_filter=True if(datetime.datetime.today() == data.index and datetime.datetime.today().hour <= 12) else False)
            self.write_list(location.fcast_max_temp, data['TEMP_MAX'], location.store_data, item_filter=True if(datetime.datetime.today() == data.index and datetime.datetime.today().hour <= 12) else False)
            self.write_list(location.obs_max_temp, data['TEMP_MAX'], location.store_data, item_filter=False if(datetime.datetime.today() == data.index and datetime.datetime.today().hour <= 12) else True)
                
