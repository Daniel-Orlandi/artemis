import datetime
import json
from pathlib import Path

def check_exists(filename: str = None, dir_path: str = None) -> bool:

  if(isinstance(filename, str)):
    if (Path(filename).is_file()):
      return True    

  elif(isinstance(dir_path, str)):
    if (Path(dir_path).is_dir()):
      return True
  
  else:
    return False

def check_d_type(data, fmt):
  if (isinstance(data, fmt)):
    return True
  
  else:
    raise TypeError (f'Data must be of type {fmt}.')

def check_date_format(date: str, date_format: str):
  try:
      datetime.datetime.strptime(date, date_format)

  except ValueError:
        raise ValueError(f'Incorrect data format, should be {date_format}')

def set_date_from_today(**kwargs):
  today = datetime.date.today()

  return today + datetime.timedelta(**kwargs)  

def read_json(filename: str) -> dict:
  with open(filename, 'r') as j:
    json_data = json.load(j)

    return json_data

def merge_dict(dict_list: list) -> dict:
  dict1 = {}
  for dictionary in dict_list:
    dict1.update(dictionary)
    
  return dict1

