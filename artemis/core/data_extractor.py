import numpy as np
import pandas
import utils

import unidecode


class Extractor:
    def __init__(self, data_dict: dict) -> None:
        self.data_dict = data_dict
        self.data_frame = pandas.DataFrame
        self.logger = utils.data_logger.Logger().set_logger(__name__)

    def get_data_dict(self):
        return self.data_dict

    def get_dataframe(self):
        return self.data_frame

    @staticmethod
    def get_temp(dataframe: pandas.DataFrame, mode: str) -> pandas.DataFrame:       
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

    def set_data(self, data_dict: dict) -> pandas.DataFrame:
        try:
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
                    'host not recognized, you need to add it to the aplication. Contact development.!')

            data['DATA'] =  pandas.to_datetime(data['DATA'], format='%Y-%m-%d')
            data['CIDADE'] = data['CIDADE'].apply(lambda x: unidecode.unidecode(x))

            self.logger.info('Location:{}'.format(data['CIDADE']))
            return data

        except ValueError as value_error:
            self.logger.error(f'Value Error: {value_error}')
            raise value_error

        except Exception as general_error:
            self.logger.error(f'Ops another error ocurred: {general_error}')
            raise general_error

    def run(self) -> None:        
        self.logger.info('concatenating all results in data_dict.')
        result = pandas.DataFrame()

        # aplica set_data linha a linha, pq set data foi pensado para funcionar por cidade
        for key, value in self.data_dict.items():
            df = self.set_data(value)
            result = pandas.concat([result, df])

        result[['TEMP_MAX', 'TEMP_MIN']] = result[['TEMP_MAX', 'TEMP_MIN']].apply(pandas.to_numeric)

        self.logger.info('Getting min temps.')
        temp_min = self.get_temp(result, 'TEMP_MIN')
        self.logger.info('Done getting min.')

        self.logger.info('Getting max temps.')
        temp_max = self.get_temp(result, 'TEMP_MAX')
        self.logger.info('Done getting max.')

        self.logger.info('Merging all results.')
        result = pandas.merge(temp_min, temp_max, how='outer')
        self.logger.info('Results merged!')

        result = result.rename(columns={"DATA_x": "DATA"})
        result.index = result['DATA']
        result.drop(columns={'DATA'})
        result.sort_index(inplace=True)
        result = result[['CIDADE', 'TEMP_MAX', "CD_ESTACAO_max", 'TEMP_MIN', "CD_ESTACAO_min"]]
        self.data_frame = result
        self.logger.info('Results stored!')
