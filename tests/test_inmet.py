import datetime
import asyncio
import time
import pandas
from matplotlib.cbook import flatten 

from artemis.core.http_engine import Request
from artemis.core.data_extractor import Extractor
from artemis.core.sheet_controller import WorkBook
from artemis.models.cptec import CptecApiSuite
from artemis.models.inmet import InmetApiSuite
from artemis.models.location_model import Location
from utils import read_json

start = time.perf_counter()
# my_logger = data_logger.Logger().set_logger(__name__)

file = read_json("resources/locations.json")
cities_list = []

for city in file['cities']:
    my_location = Location()
    my_location.set_location(city)
    cities_list.append(my_location)
    
id_locale_list = []
[id_locale_list.append(location.ws_id) for location in cities_list]
id_locale_list = list(flatten(id_locale_list))

model_2 = InmetApiSuite(id_locale_list=id_locale_list)
url = model_2.base_url + "/estacao/{}/{}/{}"
data_dict = model_2.set_request_dict_by_date_range(url,"2021-02-01","2021-02-02")

getter = Request(data_dict=data_dict)
asyncio.run(getter.get(method='async'))

my_extractor = Extractor(data_dict, cities_list)
my_extractor.set_locations()

my_workbook = WorkBook(location_list = cities_list,filename ="data/original_file/Telecarga_CO_2021-01-22.xlsm")
my_workbook.load_sheet(keep_vba=True, data_only=False)
my_workbook.set_active_table("Tabela")
my_workbook.set_date_cell("2021-02-02", "A1")
my_workbook.write_data_to_table() 
my_workbook.save_sheet(my_workbook.get_workbook,"teste.xlsm")

end = time.perf_counter() - start
print(end)




