
import math 
from abc import abstractmethod
from pydub import AudioSegment
from pathlib import Path 
from collections.abc import Iterable
from .object import Object, SEObject
from .file_utility import safe_stem
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .environment_holder import EnvironmentHolder

class SpeakerVoiceGenerator (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  speaker_voice_generator_type_table = {}

  def __init__ (self, *, parent, config, environment):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)

  @abstractmethod
  def make_object (self, text:str, speakervoice) -> Object:
    pass

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    if params["type"] in cls.speaker_voice_generator_type_table:
      return cls.speaker_voice_generator_type_table[params["type"]].deserialize(params, parent=parent, config=config, environment=environment)
    else:
      raise ValueError("Type {!r} is not registered in {!r}.".format(params["type"], cls)) #error 

class SimpleSpeakerVoiceGenerator (SpeakerVoiceGenerator):

  def __init__ (self, *, parent, config, environment, volume=1.0, direction=0.0, speed=1.0):
    super().__init__(parent=parent, config=config, environment=environment)
    self.volume = volume
    self.direction = direction
    self.speed = speed

  def _get_spoke_file (self, text, speakervoice):
    return Path(self.parent.config["voice_save_dir"], "{:s}_{:s}.wav".format(safe_stem(text), speakervoice.get_file_id()))

  def make_object (self, text, speakervoice):
    audiofile = self._get_spoke_file(text, speakervoice)
    speakervoice.speak(text, audiofile)
    audio = AudioSegment.from_file(audiofile)
    audioframes = math.floor(audio.duration_seconds * self.parent.framerate)
    return SEObject(
      audiofile, 
      audioframes, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      volume=self.volume, 
      direction=self.direction, 
      speed=self.speed
    )

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      volume=params.get("volume", 1.0), 
      speed=params.get("speed", 1.0)
    )
