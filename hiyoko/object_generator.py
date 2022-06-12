
import math 
from abc import abstractmethod
from pydub import AudioSegment
from exofile import Color, ShapeType, TextAlignment
from pathlib import Path 
from collections.abc import Iterable
from .object import Object, ColorBackgroundObject, ImageBackgroundObject, VideoBackgroundObject, CinemaScopeObject, SubtitleObject, BGMObject, SEObject
from .file_utility import search_file
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder 
from .deserializable import Deserializable
from .variable import StringVar, IntVar, FloatVar, BooleanVar, ColorVar
from .environment_holder import EnvironmentHolder 

class ObjectGenerator (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  object_generator_type_table = {}
  to_base_length = False 

  def __init__ (self, *, parent, config, environment):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)

  @abstractmethod
  def make_object (self, text:str, frames:int) -> Object:
    pass

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    if params["type"] in cls.object_generator_type_table:
      return cls.object_generator_type_table[params["type"]].deserialize(params, parent=parent, config=config, environment=environment)
    else:
      raise ValueError("Type {!r} is not registered in {!r}.".format(params["type"], cls)) #error 

class ColorBackgroundGenerator (ObjectGenerator):

  def __init__ (self, *, parent, config, environment):
    super().__init__(parent=parent, config=config, environment=environment)
    self.colorvar = ColorVar()
    parent.variables.register("背景色", self.colorvar)

  @property
  def color (self):
    return self.colorvar.get()

  def make_object (self, text, frames):
    if self.color:
      return ColorBackgroundObject(
        self.color, 
        frames, 
        parent=self.parent, 
        config=self.config,
        environment=self.environment,
      )
    else:
      return None 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config,
      environment=environment,
    )

class ImageBackgroundGenerator (ObjectGenerator):

  def __init__ (self, *, parent, config, environment, stretch=False):
    super().__init__(parent=parent, config=config, environment=environment)
    self.defaultstretch = stretch 
    self.filevar = StringVar()
    self.stretchvar = BooleanVar()
    parent.variables.register("背景画像", self.filevar)
    parent.variables.register("背景画像全表示", self.stretchvar)

  @property
  def file (self):
    return self.filevar.get()

  @property
  def stretch (self):
    if self.stretchvar.is_assigned():
      return self.stretchvar.get()
    else:
      return self.defaultstretch

  def make_object (self, text, frames):
    if self.file:
      foundfile = search_file(self.file, config=self.config, environment=self.environment) 
      return ImageBackgroundObject(
        Path(foundfile).absolute(), 
        frames, 
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        stretch=self.stretch,
      )
    else:
      return None

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      stretch=params.get("stretch", False),
    )

class VideoBackgroundGenerator (ObjectGenerator):

  def __init__ (self, *, parent, config, environment, stretch=False, loop=False):
    super().__init__(parent=parent, config=config, environment=environment)
    self.defaultstretch = stretch 
    self.defaultloop = loop
    self.filevar = StringVar()
    self.stretchvar = BooleanVar()
    self.loopvar = BooleanVar()
    parent.variables.register("背景動画", self.filevar)
    parent.variables.register("背景動画全表示", self.stretchvar)
    parent.variables.register("背景動画ループ", self.loopvar)

  @property
  def file (self):
    return self.filevar.get()

  @property
  def stretch (self):
    if self.stretchvar.is_assigned():
      return self.stretchvar.get()
    else:
      return self.defaultstretch

  @property
  def loop (self):
    if self.loopvar.is_assigned():
      return self.loopvar.get()
    else:
      return self.defaultloop

  def make_object (self, text, frames):
    if self.file:
      foundfile = search_file(self.file, config=self.config, environment=self.environment)
      return VideoBackgroundObject(
        Path(foundfile).absolute(), 
        frames, 
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        stretch=self.stretch,
        loop=self.loop,
      )
    else:
      return None

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      stretch=params.get("stretch", False),
      loop=params.get("loop", False),
    )

class CinemaScopeGenerator (ObjectGenerator):

  def __init__ (self, ratio, *, parent, config, environment, color=Color(0, 0, 0)):
    super().__init__(parent=parent, config=config, environment=environment)
    self.ratio = ratio
    self.color = color 

  def make_object (self, text, frames):
    return CinemaScopeObject(
      self.ratio, 
      frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      color=self.color,
    )

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      params["ratio"], 
      parent=parent, 
      config=config, 
      environment=environment,
      color=Color.deserialize(params.get("color", "000000")),
    )

class SubtitleGenerator (ObjectGenerator):

  def __init__ (self, *, parent, config, environment, x=0, y=0, font="Meiryo", size=30, color=Color(255, 255, 255)):
    super().__init__(parent=parent, config=config, environment=environment)
    self.x = x
    self.y = y
    self.defaultfont = font 
    self.defaultsize = size
    self.defaultcolor = color 
    self.fontvar = StringVar()
    self.sizevar = IntVar()
    self.colorvar = ColorVar()
    self.parent.variables.register("字幕フォント", self.fontvar)
    self.parent.variables.register("字幕サイズ", self.sizevar)
    self.parent.variables.register("字幕色", self.colorvar)

  @property 
  def font (self):
    if self.fontvar.is_assigned():
      return self.fontvar.get()
    else:
      return self.defaultfont

  @property 
  def size (self):
    if self.sizevar.is_assigned():
      return self.sizevar.get()
    else:
      return self.defaultsize

  @property 
  def color (self):
    if self.colorvar.is_assigned():
      return self.colorvar.get()
    else:
      return self.defaultcolor

  def make_object (self, text, frames):
    return SubtitleObject(
      text, 
      frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      x=self.x, 
      y=self.y, 
      font=self.font, 
      size=self.size, 
      color=self.color,
    )

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      x=params.get("x", 0), 
      y=params.get("y", 0), 
      font=params.get("font", "Meiryo"), 
      size=params.get("size", 30), 
      color=Color.deserialize(params.get("color", "ffffff")),
    )

class SEGenerator (ObjectGenerator):

  to_base_length = True #extend all next objects length.

  def __init__ (self, *, parent, config, environment, volume=1.0, direction=0.0, speed=1.0):
    super().__init__(parent=parent, config=config, environment=environment)
    self.defaultvolume = volume
    self.defaultdirection = direction
    self.defaultspeed = speed
    self.filevar = StringVar()
    self.volumevar = FloatVar()
    self.directionvar = FloatVar()
    self.speedvar = FloatVar()
    self.parent.variables.register("SE", self.filevar)
    self.parent.variables.register("SE音量", self.volumevar)
    self.parent.variables.register("SE左右", self.directionvar)
    self.parent.variables.register("SE速度", self.speedvar)

  @property
  def file (self):
    return self.filevar.get()

  @property
  def volume (self):
    if self.volumevar.is_assigned():
      return self.volumevar.get()
    else:
      return self.defaultvolume

  @property
  def direction (self):
    if self.directionvar.is_assigned():
      return self.directionvar.get()
    else:
      return self.defaultdirection

  @property
  def speed (self):
    if self.speedvar.is_assigned():
      return self.speedvar.get()
    else:
      return self.defaultspeed

  def make_object (self, text, frames): #ignore frames 
    if self.file:
      foundfile = search_file(self.file, config=self.config, environment=self.environment)
      audio = AudioSegment.from_file(foundfile)
      audioframes = math.floor(audio.duration_seconds * self.parent.framerate)
      obj = SEObject(
        Path(foundfile).absolute(), 
        audioframes, 
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        volume=self.volume, 
        direction=self.direction, 
        speed=self.speed,
      )
      self.filevar.clear()
      return obj 
    else:
      return None 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      volume=params.get("volume", 1.0), 
      direction=params.get("direction", 0.0), 
      speed=params.get("speed", 1.0),
    )

class BGMGenerator (ObjectGenerator):

  to_base_length = False #extend length with merging.

  def __init__ (self, *, parent, config, environment, volume=1.0, direction=0.0, speed=1.0, loop=False):
    super().__init__(parent=parent, config=config, environment=environment)
    self.defaultvolume = volume
    self.defaultdirection = direction
    self.defaultspeed = speed
    self.defaultloop = loop 
    self.filevar = StringVar() 
    self.volumevar = FloatVar()
    self.directionvar = FloatVar() 
    self.speedvar = FloatVar()
    self.loopvar = BooleanVar()
    self.parent.variables.register("BGM", self.filevar)
    self.parent.variables.register("BGM音量", self.volumevar)
    self.parent.variables.register("BGM左右", self.directionvar)
    self.parent.variables.register("BGM速度", self.speedvar)
    self.parent.variables.register("BGMループ", self.loopvar)

  @property
  def file (self):
    return self.filevar.get()

  @property
  def volume (self):
    if self.volumevar.is_assigned():
      return self.volumevar.get()
    else:
      return self.defaultvolume 

  @property
  def direction (self):
    if self.directionvar.is_assigned():
      return self.directionvar.get()
    else:
      return self.defaultdirection 

  @property
  def speed (self):
    if self.speedvar.is_assigned():
      return self.speedvar.get()
    else:
      return self.defaultspeed 

  @property
  def loop (self):
    if self.loopvar.is_assigned():
      return self.loopvar.get()
    else:
      return self.defaultloop 

  def make_object (self, text, frames):
    if self.file:
      foundfile = search_file(self.file, config=self.config, environment=self.environment)
      return BGMObject(
        Path(foundfile).absolute(), 
        frames, 
        parent=self.parent, 
        config=self.config, 
        environment=self.environment,
        volume=self.volume, 
        direction=self.direction, 
        speed=self.speed, 
        loop=self.loop,
      )
    else:
      return None 

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent, 
      config=config, 
      environment=environment,
      volume=params.get("volume", 1.0), 
      direction=params.get("direction", 0.0), 
      speed=params.get("speed", 1.0), 
      loop=params.get("loop", False),
    )
