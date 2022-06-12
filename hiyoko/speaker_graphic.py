
from abc import abstractmethod
from pathlib import Path 
from collections.abc import Iterable
from .object import Object, CharacterGraphicObject
from .file_utility import search_file
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .environment_holder import EnvironmentHolder 

class SpeakerGraphic (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  speaker_graphic_type_table = {}

  def __init__ (self, *, parent, config, environment, default=False):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self.default = default

  @abstractmethod
  def make_object (self, x:float, y:float, frames:int) -> Object:
    pass

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    if params["type"] in cls.speaker_graphic_type_table:
      return cls.speaker_graphic_type_table[params["type"]].deserialize(params, parent=parent, config=config, environment=environment)
    else:
      raise ValueError("Type {!r} is not registered in {!r}.".format(params["type"], cls)) #error 

class CopySpeakerGraphic (SpeakerGraphic):

  def __init__ (self, name, *, parent, config, environment, default=False):
    super().__init__(parent=parent, config=config, environment=environment, default=default)
    self.name = name 

  def _dereference (self):
    dereferenced = self.parent.speakervoices[self.name]
    if dereferenced is not self:
      if dereferenced.graphic:
        return dereferenced.graphic
      else:
        raise ValueError("Voice {!r} has no graphic.".format(self.name)) #error 
    else:
      raise ValueError("Graphic {!r} referenced itself {!r}.".format(self, self.name)) #error 

  def make_object (self, x, y, frames):
    return self._dereference().make_object(x, y, frames)

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      params["voice"], 
      parent=parent, 
      config=config, 
      environment=environment,
      default=params.get("default", False)
    )

class SimpleSpeakerGraphic (SpeakerGraphic):

  def __init__ (self, file, *, parent, config, environment, default=False, x=0, y=0, scale=1.0):
    super().__init__(parent=parent, config=config, environment=environment, default=default)
    self.file = file 
    self.x = x
    self.y = y
    self.scale = scale

  def make_object (self, x, y, frames):
    foundfile = search_file(self.file, config=self.config, environment=self.environment)
    return CharacterGraphicObject(
      Path(foundfile).absolute(),
      frames,
      parent=self.parent,
      config=self.config,
      environment=self.environment,
      x=self.x + x,
      y=self.y + y,
      scale=self.scale
    )

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      params["src"], 
      parent=parent, 
      config=config, 
      environment=environment,
      default=params.get("default", False), 
      x=params.get("x", 0), 
      y=params.get("y", 0), 
      scale=params.get("scale", 1.0)
    )
