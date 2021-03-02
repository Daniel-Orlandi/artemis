class Location:
  def __init__(self,
               name = None,
               region = None,
               cptec_id = None,               
               ws_id = None,
               row = None) -> None:

    self.name = name
    self.region = region
    self.cptec_id = cptec_id
    self.ws_id = ws_id
    self.row = None
    self.obs_min_temp = ["C","E"]
    self.obs_max_temp = ["D", "F"]
    self.fcast_min_temp = ["G","I","K"]
    self.fcast_max_temp = ["H","J","L"]   
    self.cloud_cover_w_cond = ["M", "P", "S", "V", "Y", "AB"]
    self.precip_w_cond = ["N", "Q", "T", "W", "Z", "AC"]
    self.period_w_cond = ["O", "R", "U", "X", "AA", "AD"]     
    self.data = {}
  
  def set_location(self,location_dict: dict):
    for key, value in location_dict.items():
      self.__dict__[key] = value
    
  def get_id_locale(self):
    return self.ws_id

  @staticmethod
  def remove_from_positioning_list(item, data_list:list, ignore:bool = False) -> None:
    try:
      data_list.remove(item)
    
    except ValueError as value_error:
      raise value_error

    except Exception as general_error:
      raise general_error
      
  @staticmethod
  def add_to_positioning_list(item, data_list:list) -> None:
    try:
      data_list.append(item)
    
    except ValueError as value_error:
      raise value_error

    except Exception as general_error:
      raise general_error
      

  def store_data(self, key, value) -> None:
    self.data[str(key)+str(self.row)] = value


