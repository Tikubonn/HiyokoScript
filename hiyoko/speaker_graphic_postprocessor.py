
from abc import abstractmethod
from exolib import ObjectNode, ObjectParamNode, FloatTrackBarRanges, IntTrackBarRanges
from exofile import TrackBarType, Float 
from collections.abc import Iterable
from .object import Object, BounceObject, RasterObject, HoppingObject
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .variable import SpeakersVar, FloatVar, IntVar, BooleanVar
from .environment_holder import EnvironmentHolder

class SpeakerGraphicPostProcessor (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  speaker_graphic_postprocessor_type_table = {}

  def __init__ (self, *, parent, config, environment):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)

  @abstractmethod
  def postprocess (self, text:str, obj:Object, speaker) -> Object:
    pass

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    if params["type"] in cls.speaker_graphic_postprocessor_type_table:
      return cls.speaker_graphic_postprocessor_type_table[params["type"]].deserialize(params, parent=parent, config=config, environment=environment)
    else:
      raise ValueError("Type {!r} is not registered in {!r}.".format(params["type"], cls)) #error 

class BouncePostProcessor (SpeakerGraphicPostProcessor): 

  def __init__ (self, *, parent, config, environment, crashratio=1.05, interval=0.5):
    super().__init__(parent=parent, config=config, environment=environment)
    self.defaultcrashratio = crashratio
    self.defaultinterval = interval
    self.crashratiovar = FloatVar()
    self.intervalvar = FloatVar()
    self.speakersvar = SpeakersVar(parent=parent)
    parent.variables.register("もにゅもにゅ変形比", self.crashratiovar)
    parent.variables.register("もにゅもにゅ周期", self.intervalvar)
    parent.variables.register("もにゅもにゅ", self.speakersvar)

  @property 
  def crashratio (self):
    if self.crashratiovar.is_assigned():
      return self.crashratiovar.get()
    else:
      return self.defaultcrashratio

  @property 
  def interval (self):
    if self.intervalvar.is_assigned():
      return self.intervalvar.get()
    else:
      return self.defaultinterval

  def postprocess (self, text, obj, speaker):
    if speaker in self.speakersvar.get():
      return BounceObject(
        obj, 
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        crashratio=self.crashratio, 
        interval=self.interval
      )
    else:
      return obj 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      crashratio=params.get("crash_ratio", 1.05), 
      interval=params.get("interval", 0.5)
    )

class BounceAtSpeakingPostProcessor (SpeakerGraphicPostProcessor): 

  def __init__ (self, *, parent, config, environment, crashratio=1.05, interval=0.5):
    super().__init__(parent=parent, config=config, environment=environment)
    self.crashratio = crashratio
    self.interval = interval
    self.enablevar = BooleanVar()
    parent.variables.register("自動もにゅもにゅ", self.enablevar)

  @property
  def enable (self):
    if self.enablevar.is_assigned():
      return self.enablevar.get()
    else:
      return False

  def postprocess (self, text, obj, speaker):
    if self.enable and self.parent.now_speaking(speaker):
      return BounceObject(
        obj, 
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        crashratio=self.crashratio, 
        interval=self.interval
      )
    else:
      return obj 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      crashratio=params.get("crash_ratio", 1.05), 
      interval=params.get("interval", 0.5)
    )

class HoppingPostProcessor (SpeakerGraphicPostProcessor):

  def __init__ (self, *, parent, config, environment, crashratio=1.05, height=100, interval=1.0):
    super().__init__(parent=parent, config=config, environment=environment)
    self.defaultcrashratio = crashratio
    self.defaultheight = height
    self.defaultinterval = interval
    self.crashratiovar = FloatVar()
    self.heightvar = FloatVar()
    self.intervalvar = FloatVar()
    self.speakersvar = SpeakersVar(parent=parent)
    parent.variables.register("ぴょんぴょん変形比", self.crashratiovar)
    parent.variables.register("ぴょんぴょん高さ", self.heightvar)
    parent.variables.register("ぴょんぴょん周期", self.intervalvar)
    parent.variables.register("ぴょんぴょん", self.speakersvar)

  @property 
  def crashratio (self):
    if self.crashratiovar.is_assigned():
      return self.crashratiovar.get()
    else:
      return self.defaultcrashratio

  @property 
  def height (self):
    if self.heightvar.is_assigned():
      return self.heightvar.get()
    else:
      return self.defaultheight

  @property 
  def interval (self):
    if self.intervalvar.is_assigned():
      return self.intervalvar.get()
    else:
      return self.defaultinterval

  def postprocess (self, text, obj, speaker):
    if speaker in self.speakersvar.get():
      return HoppingObject(
        obj,
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        crashratio=self.crashratio,
        height=self.height, 
        interval=self.interval
      )
    else:
     return obj

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      crashratio=params.get("crash_ratio", 1.05),
      height=params.get("height", 100), 
      interval=params.get("interval", 1.0)
    )

class HoppingAtSpeakingPostProcessor (SpeakerGraphicPostProcessor):

  def __init__ (self, *, parent, config, environment, crashratio=1.05, height=100, interval=1.0):
    super().__init__(parent=parent, config=config, environment=environment)
    self.crashratio = crashratio
    self.height = height
    self.interval = interval
    self.enablevar = BooleanVar()
    parent.variables.register("自動ぴょんぴょん", self.enablevar)

  @property
  def enable (self):
    if self.enablevar.is_assigned():
      return self.enablevar.get()
    else:
      return False

  def postprocess (self, text, obj, speaker):
    if self.enable and self.parent.now_speaking(speaker):
      return HoppingObject(
        obj,
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        crashratio=self.crashratio,
        height=self.height, 
        interval=self.interval
      )
    else:
     return obj

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      crashratio=params.get("crash_ratio", 1.05),
      height=params.get("height", 100), 
      interval=params.get("interval", 1.0)
    )

class RasterPostProcessor (SpeakerGraphicPostProcessor):

  def __init__ (self, *, parent, config, environment, width=100, height=100, interval=1.0):
    super().__init__(parent=parent, config=config, environment=environment)
    self.defaultwidth = width
    self.defaultheight = height
    self.defaultinterval = interval
    self.widthvar = IntVar()
    self.heightvar = IntVar()
    self.intervalvar = FloatVar()
    self.speakersvar = SpeakersVar(parent=parent)
    parent.variables.register("ぐにゃぐにゃ横幅", self.widthvar)
    parent.variables.register("ぐにゃぐにゃ縦幅", self.heightvar)
    parent.variables.register("ぐにゃぐにゃ周期", self.intervalvar)
    parent.variables.register("ぐにゃぐにゃ", self.speakersvar)

  @property 
  def width (self):
    if self.widthvar.is_assigned():
      return self.widthvar.get()
    else:
      return self.defaultwidth

  @property 
  def height (self):
    if self.heightvar.is_assigned():
      return self.heightvar.get()
    else:
      return self.defaultheight

  @property 
  def interval (self):
    if self.intervalvar.is_assigned():
      return self.intervalvar.get()
    else:
      return self.defaultinterval

  def postprocess (self, text, obj, speaker):
    if speaker in self.speakersvar.get():
      return RasterObject(
        obj,
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        width=self.width, 
        height=self.height, 
        interval=self.interval
      )
    else:
     return obj

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      width=params.get("width", 100), 
      height=params.get("height", 100), 
      interval=params.get("interval", 1.0)
    )
