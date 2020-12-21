from api import data_getter
from models.cptec import CptecApiSuite
from utils import data_logger
import asyncio

logger = data_logger.Logger(filename='log_file.log',                                                        
                            log_format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")

my_logger = logger.set_logger(__name__)
data_model = CptecApiSuite()

data = data_model.get_current_weather_condition_capitals()

getter = data_getter.Request(url_dict=data)

asyncio.run(getter.get_data(method='a'))

print(getter.url_dict)

my_logger.info('Done')