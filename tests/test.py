import asyncio
import time
import pandas
import artemis.core.response_handler as response_handler
from artemis.core.http_engine import Request
from artemis.core.data_extractor import Extractor
from artemis.models.cptec import CptecApiSuite
from artemis.utils import data_logger

start = time.perf_counter()

model = CptecApiSuite(id_locale_list=[244, 241])
data_dict = model.get_forecast_by_date_delta(num_days='4days')

getter = Request(data_dict=data_dict)
asyncio.run(getter.get(method='async'))

my_extractor = Extractor(data_dict)
data_dict = my_extractor.get_data()
workbook = my_extractor.load_sheet(filename="Telecarga_SUL_2021-01-13 copy.xlsm", keep_vba=True, data_only=False)

for key, value in data_dict.items():
    df = my_extractor.set_data(value)
    my_extractor.to_xlsx(workbook, dataframe=df, data_type='forecast')

my_extractor.save_sheet(
    workbook, out_file="data/result/Telecarga_SUL_2021-01-13.xlsm")

end = time.perf_counter() - start
print('end')
