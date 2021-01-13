import asyncio
import time
import pandas
import artemis.core.response_handler as response_handler
from artemis.core.http_engine import Request
from artemis.core.data_extractor import Extractor
from artemis.models.cptec import CptecApiSuite
from utils import data_logger

start = time.perf_counter()
my_logger = data_logger.Logger().set_logger(__name__)

data = CptecApiSuite([244,241]).get_forecast('4days')
getter = Request(data_dict=data)
await getter.data(method='a')

my_extractor = Extractor(data)
data_dict = my_extractor.get_data()
workbook = my_extractor.load_sheet(filename="data/original_file/Telecarga_SUL_2021-01-13.xlsx")

for key, value in data_dict.items():
    df = my_extractor.set_data(value)    
    my_extractor.to_xlsx(workbook, dataframe = df, data_type='forecast')

my_extractor.save_sheet(workbook, out_file="data/result/Telecarga_SUL_2021-01-13.xlsx")    

end = time.perf_counter() - start
print('end')

