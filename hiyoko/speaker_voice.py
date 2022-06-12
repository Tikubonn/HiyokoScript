
import os 
import re 
import time 
import json #VOICEVOX-APIではより厳格なjsonを使用します。json5は使用しません。
import requests 
import subprocess
from io import StringIO
from abc import abstractmethod
from enum import IntEnum, auto, unique
from pathlib import Path 
from .file_utility import create_file
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .speaker_graphic import SpeakerGraphic
from .environment_holder import EnvironmentHolder

class SpeakerVoice (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  speaker_voice_type_table = {}

  def __init__ (self, *, parent, config, environment, graphic=None):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self.graphic = graphic

  @abstractmethod
  def get_file_id (self) -> str:
    pass

  @abstractmethod
  def speak (self, text:str, file:Path) -> None:
    pass

  @classmethod
  def deserialize_graphic (cls, params, *, parent, config, environment):
    if "graphic" in params:
      return SpeakerGraphic.deserialize(params["graphic"], parent=parent, config=config, environment=environment)
    else:
      return None 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    if params["type"] in cls.speaker_voice_type_table:
      return cls.speaker_voice_type_table[params["type"]].deserialize(params, parent=parent, config=config, environment=environment)
    else:
      raise ValueError("Type {!r} is not registered in {!r}.".format(params["type"], cls)) #error 

class CopySpeakerVoice (SpeakerVoice):

  def __init__ (self, name, *, parent, config, environment, graphic=None):
    super().__init__(parent=parent, config=config, environment=environment, graphic=graphic)
    self.name = name 

  def _dereference (self):
    dereferenced = self.parent.speakervoices[self.name]
    if dereferenced is not self:
      return dereferenced
    else:
      raise ValueError("Voice {!r} referenced itself {!r}.".format(self, self.name)) #error

  def get_file_id (self):
    return self._dereference().get_file_id()

  def speak (self, text, file):
    return self._dereference().speak(text, file)

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      params["voice"], 
      parent=parent, 
      config=config, 
      environment=environment,
      graphic=cls.deserialize_graphic(params, parent=parent, config=config, environment=environment)
    )

#voicevox 

class VoiceVoxSpeakerVoiceStyle:

  NORMAL = "ノーマル"
  SWEET = "あまあま"
  TSUNTSUN = "ツンツン"
  SEXY = "セクシー"

class VoiceVoxSpeakerVoice (SpeakerVoice):

  _cached_speakers = None
  _cached_id = None 

  def __init__ (self, name, style=VoiceVoxSpeakerVoiceStyle.NORMAL, *, parent, config, environment, graphic=None, speedscale=1.0, pitchscale=0.0, intonationscale=1.0, volumescale=1.0):
    SpeakerVoice.__init__(self, parent=parent, config=config, environment=environment, graphic=graphic)
    self.name = name 
    self.style = style
    self.speedscale = speedscale
    self.pitchscale = pitchscale
    self.intonationscale = intonationscale
    self.volumescale = volumescale

  def _load_speakers (self, *, reload=False):
    if type(self)._cached_speakers is None or reload:
      req = requests.get("http://{:s}:{:d}/speakers".format(self.config["voicevox"]["host"], self.config["voicevox"]["port"]))
      req.raise_for_status()
      speakers = json.loads(req.text)
      type(self)._cached_speakers = speakers

  def _find_speaker_id (self, name, style, *, reload=False):
    self._load_speakers(reload=reload)
    for speaker in type(self)._cached_speakers:
      if speaker["name"] == name:
        for speakerstyle in speaker["styles"]:
          if speakerstyle["name"] == style:
            return speakerstyle["id"]
    else:
      raise ValueError("Could not find speaker of {:s}:{:s}.".format(self.name, self.style)) #error

  def get_id (self, *, reload=False):
    if self._cached_id is None or reload:
      self._cached_id = self._find_speaker_id(self.name, self.style, reload=reload)
    return self._cached_id

  def get_file_id (self):
    return "voicevox{:d}".format(self.get_id())

  def speak (self, text, file):
    req1 = requests.post("http://{:s}:{:d}/audio_query".format(self.config["voicevox"]["host"], self.config["voicevox"]["port"]), params={ "text": text, "speaker": self.get_id() })
    req1.raise_for_status()
    query = req1.json()
    query["speedScale"] = self.speedscale
    query["pitchScale"] = self.pitchscale
    query["intonationScale"] = self.intonationscale
    query["volumeScale"] = self.volumescale
    req2 = requests.post("http://{:s}:{:d}/synthesis".format(self.config["voicevox"]["host"], self.config["voicevox"]["port"]), params={ "speaker": self.get_id() }, data=json.dumps(query).encode("utf-8"))
    req2.raise_for_status()
    with create_file(file, "wb", createdirectories=True, directoriesexistok=True) as stream:
      stream.write(req2.content)

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      params["name"], 
      params.get("style", VoiceVoxSpeakerVoiceStyle.NORMAL), 
      parent=parent, 
      config=config, 
      environment=environment,
      graphic=cls.deserialize_graphic(params, parent=parent, config=config, environment=environment), 
      speedscale=params.get("speed_scale", 1.0), 
      pitchscale=params.get("pitch_scale", 0.0), 
      intonationscale=params.get("intonation_scale", 1.0), 
      volumescale=params.get("volume_scale", 1.0)
    )

#softalk

@unique
class SoftalkSpeakerVoiceNameType (IntEnum):

  VOICE_NAME = auto()
  PRESET_NAME = auto()

class SoftalkSpeakerVoiceName (Deserializable):

  def __init__ (self, name, nametype=SoftalkSpeakerVoiceNameType.VOICE_NAME):
    self.name = name 
    self.nametype = nametype

  def get_params (self):
    if self.nametype == SoftalkSpeakerVoiceNameType.VOICE_NAME:
      return [ "/NM:{:s}".format(self.name) ]
    elif self.nametype == SoftalkSpeakerVoiceNameType.PRESET_NAME:
      return [ "/PR:{:s}".format(self.name) ]
    else:
      raise ValueError("Unknown type {!r} received.".format(self.nametype)) #error 

  def get_file_id (self):
    if self.nametype == SoftalkSpeakerVoiceNameType.VOICE_NAME:
      return "softalk{:s}".format(self.name)
    elif self.nametype == SoftalkSpeakerVoiceNameType.PRESET_NAME:
      return "softalk-preset{:s}".format(self.name)
    else:
      raise ValueError("Unknown type {!r} received.".format(self.nametype)) #error 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    if "preset" in params:
      return SoftalkSpeakerVoiceName(params["preset"], SoftalkSpeakerVoiceNameType.PRESET_NAME)
    elif "name" in params:
      return SoftalkSpeakerVoiceName(params["name"], SoftalkSpeakerVoiceNameType.VOICE_NAME)
    else:
      raise ValueError("{!r} require `preset` or `name` parameter.".format(cls)) #error

class SoftalkSpeakerVoice (SpeakerVoice):

  def __init__ (self, name, *, parent, config, environment, graphic=None, volume=1.0, speed=1.0, pitch=1.0):
    super().__init__(parent=parent, config=config, environment=environment, graphic=graphic)
    self.name = name
    self.volume = volume
    self.speed = speed
    self.pitch = pitch

  def get_file_id (self):
    return self.name.get_file_id()

  def speak (self, text, file):
    f = Path(file)
    os.makedirs(f.parent, exist_ok=True)
    command = [ self.config["softalk"]["softalkw_exe_path"] ] + self.name.get_params() + [ 
      "/V:{:d}".format(round(self.volume * 100)), 
      "/S:{:d}".format(round(self.speed * 100)), 
      "/O:{:d}".format(round(self.pitch * 100)), 
      "/R:{:s}".format(str(f.absolute())),
      "/X:1",
      "/W:{:s}".format(str(text)),
    ]
    subprocess.run(command, shell=True, check=True)

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      SoftalkSpeakerVoiceName.deserialize(params, parent=parent, config=config, environment=environment), 
      parent=parent, 
      config=config, 
      environment=environment,
      graphic=cls.deserialize_graphic(params, parent=parent, config=config, environment=environment), 
      volume=params.get("volume", 1.0), 
      speed=params.get("speed", 1.0), 
      pitch=params.get("pitch", 1.0),
    )

#assistant seika

class AssistantSeikaSpeakerVoice (SpeakerVoice):

  _cached_speakers = None

  def __init__ (self, name, *, parent, config, environment, graphic=None, volume=None, speed=None, pitch=None, alpha=None, intonation=None, emotions={}):
    super().__init__(parent=parent, config=config, environment=environment, graphic=graphic)
    self.name = name
    self.volume = volume
    self.speed = speed
    self.pitch = pitch
    self.alpha = alpha
    self.intonation = intonation
    self.emotions = emotions

  def _load_speakers (self, *, reload=False):
    if type(self)._cached_speakers is None or reload:
      process = subprocess.run([ self.config["assistant_seika"]["seika_say2_exe_path"], "-list" ], shell=True, check=True, text=True, stdout=subprocess.PIPE)
      speakers = dict()
      with StringIO(process.stdout) as stream:
        for line in stream:
          li = line.strip()
          matchresult = re.match(r"(\d+)\s+(\S+)\s+-\s+(\S+)$", li)
          if matchresult:
            cid, speaker, application = matchresult.groups()
            speakers[speaker] = int(cid)
      type(self)._cached_speakers = speakers

  def _find_speaker_id (self, name, *, reload=False):
    self._load_speakers(reload=reload)
    return type(self)._cached_speakers[name]

  def get_cid (self, *, reload=False):
    return self._find_speaker_id(self.name)

  def get_file_id (self):
    return "assistant-seika{:d}".format(self.get_cid())

  def speak (self, text, file):
    f = Path(file)
    os.makedirs(f.parent, exist_ok=True)
    command = [ self.config["assistant_seika"]["seika_say2_exe_path"], "-cid", str(self.get_cid()) ]
    if self.volume:
      command += [ "-volume", str(self.volume) ]
    if self.speed:
      command += [ "-speed", str(self.speed) ]
    if self.pitch:
      command += [ "-pitch", str(self.pitch) ]
    if self.alpha:
      command += [ "-alpha", str(self.alpha) ]
    if self.intonation:
      command += [ "-intonation", str(self.intonation) ]
    if self.emotions:
      for name, value in self.emotions.items():
        command += [ "-emotion", str(name), str(value) ]
    command += [ "-save", f.absolute() ]
    command += [ "-t", text ]
    process = subprocess.run(command, shell=True, check=True)

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      params["name"], 
      parent=parent, 
      config=config, 
      environment=environment,
      graphic=cls.deserialize_graphic(params, parent=parent, config=config, environment=environment), 
      volume=params.get("volume", None), 
      speed=params.get("speed", None), 
      pitch=params.get("pitch", None), 
      alpha=params.get("alpha", None), 
      intonation=params.get("intonation", None), 
      emotions=params.get("emotions", {}),
    )
