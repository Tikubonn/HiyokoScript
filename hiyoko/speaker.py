
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .speaker_voice import SpeakerVoice
from .environment_holder import EnvironmentHolder 

class Speaker (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  def __init__ (self, *, parent, config, environment):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self._speakervoices = dict() 

  def add_speaker_voice (self, name, speakervoice):
    self._speakervoices[name] = speakervoice

  def remove_speaker_voice (self, name):
    del self._speakervoices[name]

  @property
  def speakervoices (self):
    return self._speakervoices.copy()

  def get_default_graphic (self):
    for speakervoice in self._speakervoices.values():
      if speakervoice.graphic and speakervoice.graphic.default:
        return speakervoice.graphic
    else:
      return None 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    speaker = Speaker(parent=parent, config=config, environment=environment)
    for name, speakervoice in params.get("voices", {}).items():
      spkervoice = SpeakerVoice.deserialize(speakervoice, parent=parent, config=config, environment=environment)
      speaker.add_speaker_voice(name, spkervoice)
    return speaker
