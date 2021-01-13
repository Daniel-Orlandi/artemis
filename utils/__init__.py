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
