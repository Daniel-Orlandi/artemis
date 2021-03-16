from artemis.utils import data_logger
from artemis import utils
from artemis.app import Carga
from artemis.utils import data_logger, merge_dict
from datetime import datetime, timedelta


logger = data_logger.Logger(__name__).get_logger()

logger.info('Beggining aplication.')

logger.info('Reading config files.')
configs = utils.read_json('/home/mdata/planilhas_carga/carga/resources/config_files/config.json')
wconfigs = utils.read_json('/home/mdata/planilhas_carga/carga/resources/config_files/weather_cond_combos.json')
logger.info('Initializing aplication.')
my_worker = Carga(date_begin=(datetime.today() - timedelta(1)).strftime('%Y-%m-%d'),
                            date_end=datetime.today().strftime('%Y-%m-%d'),
                            location_file_list=configs['files']["location_file_list"],
                            input_excel_file_list=configs['files']['excel_input_files_list'],
                            output_excel_file_list=configs['files']['excel_output_files_list'],
                            obs_host_list=configs['hosts']['obs_host_list'], 
                            fcast_host_list=configs['hosts']['fcast_host_list'],
                            cloud_cover_wcond_list=wconfigs['nebulosidade'],
                            precipitation_wcond_list=wconfigs['precipitacao'],
                            period_wcond_list=wconfigs['periodo'])


logger.info('Setting locations.')
for location_file, input_file, save_file in list(zip(my_worker.location_file_list, my_worker.input_excel_file_list, my_worker.output_excel_file_list)):
  my_worker.set_locations(location_file)

  dict_list1 = my_worker.multi_run(my_worker.obs_host_list,my_worker.make_observation)
  dict_list2 = my_worker.multi_run(my_worker.fcast_host_list,my_worker.make_forecast)  

  new_data_dict = merge_dict(dict_list1 + dict_list2)

  my_worker.set_data_dict(new_data_dict)

  logger.info('Writing to excel.')
  my_worker.write_to_excel(input_file, save_file)

  logger.info('Done.')


