import asyncio
import time
from urllib.parse import urlparse
import artemis.core.response_handler as response_handler
from artemis.core.http_engine import Request
from artemis.models.cptec import CptecApiSuite
from utils import data_logger

start = time.perf_counter()
my_logger = data_logger.Logger(filename='log_file.log',
                               log_format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s").set_logger(__name__)

data_model = CptecApiSuite([244,241])

url = data_model.get_forecast('4days')

getter = Request(url_dict=url)

asyncio.run(getter.get_data(method='a'))

my_logger.info('Done')

end = time.perf_counter() - start
print(end)


