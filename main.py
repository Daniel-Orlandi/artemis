from src.crawler import get_weather_data
from src.models.cptec import CptecApiSuite

data_model = CptecApiSuite()
print (data_model.get_current_weather_condition_capitals())
getter = get_weather_data.Request(
    'http://servicos.cptec.inpe.br/XML/cidade/244/estendida.xml')

data = getter.get_data()
