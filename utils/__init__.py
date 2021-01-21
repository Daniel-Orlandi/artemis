import datetime
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


def check_date_format(date: str, date_format: str):
  try:
        datetime.datetime.strptime(date, date_format)

  except ValueError:
        raise ValueError(f'Incorrect data format, should be {date_format}')


