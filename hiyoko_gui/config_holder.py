
from hiyoko import ConfigHolder as CHolder

class ConfigHolder (CHolder):

  @property
  def hiyokoconfig (self): #avoid conflict to Tk.config.
    return CHolder.config.fget(self)
