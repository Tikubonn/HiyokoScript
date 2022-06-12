
from abc import abstractmethod
from exolib import ObjectNode
from collections.abc import Iterable
from .object import Object
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .environment_holder import EnvironmentHolder

class SpeakerGraphicGenerator (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  speaker_graphic_generator_type_table = {}

  def __init__ (self, *, parent, config, environment):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)

  @abstractmethod
  def make_object (self, text:str, frames:int, speaker) -> Object:
    pass

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    if params["type"] in cls.speaker_graphic_generator_type_table:
      return cls.speaker_graphic_generator_type_table[params["type"]].deserialize(params, parent=parent, config=config, environment=environment)
    else:
      raise ValueError("Type {!r} is not registered in {!r}.".format(params["type"], cls)) #error 

class SimpleSpeakerGraphicGenerator (SpeakerGraphicGenerator):

  def __init__ (self, *, parent, config, environment, x=0, y=0):
    super().__init__(parent=parent, config=config, environment=environment)
    self.x = x 
    self.y = y

  def _calculate_draw_position (self, speaker):
    index = self.parent.curspeakers.index(speaker)
    x = self.parent.width / (1 + len(self.parent.curspeakers)) * (1 + index) - self.parent.width / 2.0
    y = 0.0
    return (x, y)

  def _find_speaker_graphic (self, speaker):
    for speakervoice in self.parent.curspeakervoices:
      if speakervoice in speaker.speakervoices.values():
        if speakervoice.graphic:
          return speakervoice.graphic
    else:
      return speaker.get_default_graphic()

  def make_object (self, text, frames, speaker):
    x, y = self._calculate_draw_position(speaker)
    speakergraphic = self._find_speaker_graphic(speaker)
    if speakergraphic:
      obj = speakergraphic.make_object(self.x + x, self.y + y, frames)
      return obj
    else:
      return None 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      x=params.get("x", 0), 
      y=params.get("y", 0)
    )
