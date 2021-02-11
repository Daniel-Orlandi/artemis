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
    self.obs_min = ["C","E"]
    self.obs_max = ["D","F"]
    self.fcast_temp_min = ["G","I","K"]
    self.fcast_temp_max = ["H","J","L"]   
    self.col_range_w_cond = ["M","N","O","P","Q","R","S","T","U","W","X","Y","Z","AA","AB","AD","AF","AG"]
    self.data = {}
  
  def set_location(self,location_dict: dict):
    for key, value in location_dict.items():
      self.__dict__[key] = value
    
  def get_id_locale(self) -> list:
    return self.ws_id

  def store_data(self, key, value) -> None:
    self.data[str(key)+str(self.row)] = value


