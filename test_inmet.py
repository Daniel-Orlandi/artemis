import asyncio
import time
import pandas
import artemis.core.response_handler as response_handler
from artemis.core.http_engine import Request
from artemis.core.data_extractor import Extractor
from artemis.models.inmet import InmetApiSuite
from utils import data_logger

start = time.perf_counter()
# my_logger = data_logger.Logger().set_logger(__name__)

model = InmetApiSuite(id_locale_list=['A001','A002'])
url = model.base_url + "/estacao/diaria/{}/{}/{}"
data_dict = model.set_request_dict_by_date_range(url,"2021-01-19","2021-01-19")

getter = Request(data_dict=data_dict)
asyncio.run(getter.get(method='async'))

my_extractor = Extractor(data_dict)
data_dict = my_extractor.get_data()
workbook = my_extractor.load_sheet(
    filename="Telecarga_SUL_2021-01-13 copy.xlsm", keep_vba=True, data_only=True)

for key, value in data_dict.items():
    df = my_extractor.set_data(value)
    my_extractor.to_xlsx(workbook, dataframe=df, data_type='observat')

my_extractor.save_sheet(
    workbook, out_file="data/result/Telecarga_SUL_2021-01-13.xlsm")

end = time.perf_counter() - start
print('end')
