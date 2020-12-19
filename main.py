from src.crawler import get_weather_data
from src.models.cptec import CptecApiSuite
from src.utils import data_logger

logger = data_logger.Logger(filename='log_file.log',                                                        
                            log_format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")

my_logger = logger.set_logger(__name__)
data_model = CptecApiSuite()

my_logger.info(data_model.get_current_weather_condition_capitals())
getter = get_weather_data.Request(
    'http://servicos.cptec.inpe.br/XML/cidade/244/estendida.xml')

data = getter.get_data()

my_logger.info('Done')