from artemis.utils import data_logger
from artemis import utils
from artemis import app
from artemis.utils import data_logger, merge_dict


logger = data_logger.Logger(__name__).get_logger()

logger.info('Beggining aplication.')

logger.info('Reading config files.')
configs = utils.read_json('resources/config_files/config.json')

logger.info('Initializing aplication.')
my_worker = app.MainFactory(date_begin=configs['dates']['date_begin'],
                            date_end=configs['dates']['date_end'],
                            input_excel_file_list=configs['files']['excel_input_files_list'],
                            output_excel_file_list=configs['files']['excel_output_files_list'])

logger.info('Setting locations.')
my_worker.set_locations('resources/locations.json')

logger.info('Geting obs.')
dict1 = my_worker.make_observation(host="cptec")

logger.info('Getting forecast.')
dict2 = my_worker.make_forecast(host="cptec")

new_data_dict = merge_dict([dict1, dict2])

my_worker.set_data_dict(new_data_dict)

logger.info('Writing to excel.')
my_worker.write_to_excel()


