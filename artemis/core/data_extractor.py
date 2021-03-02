import numpy as np
from openpyxl.descriptors.base import Bool
import pandas
import unidecode
from datetime import datetime

from artemis.utils import check_d_type
from artemis.utils.data_logger import Logger

class Extractor:
    """
         Extractor class to normalize data from requests made to different
         weather dataa providers.         

        Attributes
        ----------
            data_dict: dict
                dictionary containing data from providers.

            self.__data_frame: pandas.DataFrame
                dataframe where data will be stored after processing.

            self.__location_list: list of Location objects
                data from dataframe will be location-wise
                selected and stored in location objects

            self.logger: utils.data_logger
                logger initializator

            self.todays_date 
            
        Returns
        ----------
        None

        Methods
        ----------
        get_data_dict(self)

        get_dataframe(self)

        get_location_list(self)

        write_list(self, data_list, data, func)

        set_base_dataframe(self)

        overlaping_day_solver(self, data)

        get_temp(dataframe: pandas.DataFrame, mode: str) -> pandas.DataFrame:

        set_site(self, data_dict: dict) -> pandas.DataFrame:

        set_carga(self) -> None:

        """  
    def __init__(self, data_dict: dict, location_list: list) -> None:
        self.__data_dict = data_dict
        self.__data_frame = pandas.DataFrame
        self.__location_list = location_list
        self.logger = Logger(logger_name=__name__).get_logger()
        self.todays_date = datetime.today()

    @property
    def get_data_dict(self) -> dict:
        #Returns data contained in __data_dict       
        return self.__data_dict

    @property
    def get_dataframe(self) -> pandas.DataFrame:
        #Returns data contained in __data_frame
        return self.__data_frame
    
    @property
    def get_location_list(self) -> list:
        #Returns data contained in __location_list
        return self.__location_list
        
    def write_list(self, data_list, data, func):     
            for idx, item in enumerate(data_list):
                try:                                             
                    func(item,data[idx])

                except:
                    self.logger.warning(f'No data found!')
                    func(item,str("nan"))

    def set_base_dataframe(self) -> pandas.DataFrame:
        """
         Wraper method for generate base dataframe from dict.         

        Parameters
        ----------
        self       
            
        Returns
        ----------
        pandas.Dataframe
            dataframe containing selected data for given location.

        Raises
        ----------
        TypeError
            for empty data in dictionary

        ValueError
            {value} empty, skipping.

        Exception
            general error
        """  
        result = pandas.DataFrame()
        # aplica set_site linha a linha, pq set data foi pensado para funcionar por cidade
        for key, value in self.__data_dict.items():
            try:                       
                df = self.set_site(value)
                self.logger.info('Location:{}'.format(df['CIDADE']))
                result = pandas.concat([result, df])

            except TypeError as type_error:
                self.logger.warning(f'TypeError: {type_error}')
                pass

            except Exception as general_error:
                self.logger.error(f'Error: {general_error}')
                raise

        return result

    def overlaping_day_solver(self, data) -> pandas.DataFrame:
        """
         method responsible to solve overlaping current day in dataframe. This method expects
         dataframe format to be:['DATA','TEMP_MAX', 'TEMP_MIN'] shape = (2,3), with only one location per df,
         with no duplicates. The method select current day based on todays_date, and copy temp_max, from forecast line to
         obs line(expected to be the first occurence in data)
         

        Parameters
        ----------
        data: pandas.Dataframe
            dataframe containing temperature data to be extracted.      
            
        Returns
        ----------
        pandas.Dataframe
            dataframe containing selected data for given location.

        Raises
        ----------
        ValueError
            Shape not as expected. Expected (2,3) got {data.shape}

        ValueError
            {value} empty, skipping.

        Exception
            f'Error: {overlaping_general_error} (general error.)
        """  
        temp_data = data             
        try:
            #Caso 1 onde obs e previsão se encontram, pega fcast_max dia, e coloca na linha,
            #obss. Despreza linhas só com fcast 
            if(self.todays_date.hour < 15):
                data = data[data.index == self.todays_date]
                if (data.shape != (2,3)):                                        
                   raise ValueError(f"Shape not as expected. Expected (2,3) got {data.shape}")                   

                data.reset_index(inplace=True)

                value = data['TEMP_MAX'].loc[data['TEMP_MAX'] != 'NaN'].max()
                if (not value):
                   raise ValueError(f"{value} empty, skipping.")               
                
                data['TEMP_MAX'][0] = value
                data = data.drop(data.index[1])               
                
            #Caso 2, tem todas as obss, despreza linha com fcasts para o dia,                
            else:                 
                 data = data[data.index == self.todays_date]
                
                 if (data.shape != (2,3)):
                    raise ValueError(f"Shape not as expected. Expected (2,3) got {data.shape}")

                 data.reset_index(inplace=True)                 
                 data = data.drop(data.index[1])
                
            data.set_index('DATA', inplace=True) 
            return data

        except ValueError as overlaping_exception:
            self.logger.warning(f'Nothing to delete: {overlaping_exception}')                     
            return temp_data         
     
        except Exception as overlaping_general_error:
            self.logger.warning(f'Error: {overlaping_general_error}')            
            raise overlaping_general_error      
                       
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
            

    def set_carga(self) -> None:
        """
         wraper method responsible process request data, and store it in each location
         in location_list

        Parameters
        ----------
        None

        Returns
        ----------
        None       

        """        
        self.logger.info('Beggining data extraction')
        result = self.set_base_dataframe()

        #Mudando dtypr de str para float nas colunas 'TEMP_MAX' e 'TEMP_MIN'
        result[['TEMP_MAX', 'TEMP_MIN']] = result[['TEMP_MAX', 'TEMP_MIN']].apply(pandas.to_numeric)
        
        #Pegando temps max e min
        temp_min = self.get_temp(result, 'TEMP_MIN').drop_duplicates()
        temp_min.drop(columns={'CD_ESTACAO_min'}, inplace=True)
        self.logger.info(temp_min)
        self.logger.info('Done getting min.')
        
        temp_max = self.get_temp(result, 'TEMP_MAX').drop_duplicates()
        temp_max.drop(columns={'CD_ESTACAO_max'}, inplace=True)
        self.logger.info(temp_max)
        self.logger.info('Done getting max.')         
        
        #Setando DATA como index
        result = temp_min.merge(temp_max, how='left')              
        result.set_index('DATA', inplace=True)        
        result.sort_index(inplace=True)   
        result = result[['CIDADE', 'TEMP_MAX','TEMP_MIN']]
        self.__data_frame = result.drop_duplicates()
        print (self.__data_frame)

        #Escreve os dados em location.data, dicionário utilizado para escrever na planilha excel.
        for location in self.__location_list:            
            data = self.__data_frame[self.__data_frame['CIDADE'] == location.name]            
            data = self.overlaping_day_solver(data)
            self.write_list(location.obs_min_temp + location.fcast_min_temp, data['TEMP_MIN'], location.store_data)
            self.write_list(location.obs_max_temp + location.fcast_max_temp, data['TEMP_MAX'], location.store_data)
               
        self.logger.info('Done')

    

    
                
