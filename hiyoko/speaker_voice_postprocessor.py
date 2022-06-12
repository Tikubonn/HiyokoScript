
from abc import abstractmethod
from collections.abc import Iterable
from .object import Object
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .environment_holder import EnvironmentHolder

class SpeakerVoicePostProcessor (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  speaker_voice_postprocessor_type_table = {}

  def __init__ (self, *, parent, config, environment):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)

  @abstractmethod
  def postprocess (self, text:str, obj:Object, speakervoice) -> Object:
    pass

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    if params["type"] in cls.speaker_voice_postprocessor_type_table:
      return cls.speaker_voice_postprocessor_type_table[params["type"]].deserialize(params, parent=parent, config=config, environment=environment)
    else:
      raise ValueError("Type {!r} is not registered in {!r}.".format(params["type"], cls)) #error 
