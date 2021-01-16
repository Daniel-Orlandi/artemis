import multiprocessing
import numpy as np
import pandas
import utils
import multiprocessing
import os

from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows


class Extractor:
    def __init__(self, data_dict: dict) -> None:
        self.data_dict = data_dict
        self.logger = utils.data_logger.Logger().set_logger(__name__)

    def get_data(self):
        return self.data_dict

    @staticmethod
    def set_data(data_dict: dict) -> pandas.DataFrame:
        host = data_dict['host']
        data = data_dict['data']

        base = pandas.DataFrame.from_dict(data, orient='index')

        if (host == 'servicos.cptec.inpe.br'):
            data = pandas.DataFrame(base['previsao'][0])
            data['cidade'] = base['nome']['cidade']

        elif(host == 'abc'):
            pass

        else:
            raise ValueError(
                'host not recognized, you need to add it to the aplication. Contact development.!')

        return data

    @staticmethod
    def to_xlsx(workbook, dataframe: pandas.DataFrame, data_type: str):
        try:
            if (isinstance(data_type, str)):
                # Creates a new sheet in xlsx file with name = data_type
                if (data_type == 'forecast'):
                    if ('forecast' in workbook.sheetnames):
                        pass
                    else:
                        sheet = workbook.create_sheet('forecast')

                    sheet = workbook['forecast']

                elif(data_type == 'observation'):
                    if ('observation' in workbook.sheetnames):
                        pass
                    else:
                        sheet = workbook.create_sheet('observation')

                    sheet = workbook['observation']
            else:
                raise ValueError(f'Error while creating sheet inside workbook')

            for row in dataframe_to_rows(dataframe, index=False, header=True):
                sheet.append(row)

            return workbook

        except Exception as error:
            raise error

    def load_sheet(self, filename: str, **kwargs):
        try:
            self.logger.info(f'Trying to read sheet at: {filename}')
            if (utils.check_exists(filename=filename) == False):
                raise OSError
            
            if (kwargs.get('keep_vba') is not None):
                workbook = load_workbook(filename, keep_vba=kwargs.pop('keep_vba'), data_only=kwargs.pop('data_only'))

            else:
                workbook = load_workbook(filename, data_only=kwargs.pop('data_only'))

            self.logger.info(f'Done.')
            return workbook

        except OSError as os_error:
            self.logger.error(f'OS Error: {os_error}')
            raise os_error

        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise os_error

    def save_sheet(self, workbook, out_file: str):
        try:
            path = os.path.dirname(out_file)
            self.logger.info(f'Saving file at: {path}')

            if (utils.check_exists(dir_path=path) == False):
                self.logger.warning(
                    f'Folder specified to save file does not exits, creating it.')
                os.makedirs(path)
                self.logger.warning(f'Done.')

            workbook.save(out_file)

        except OSError as os_error:
            self.logger.error(f'OS Error: {os_error}')
            raise error

        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error

    # def run(self, num_worker: int):
    #     queue=multiprocessing.Queue()
    #     process=multiprocessing.Process(
    #         target=self.set_data, args=(self.data_dict))
    #     process.start()
    #     process.join()

    # amentar o multiprocessing
