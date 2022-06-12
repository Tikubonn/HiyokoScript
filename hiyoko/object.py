
import cv2
from abc import ABC, abstractmethod
from exolib import ObjectNode, ObjectParamNode, TextParamNode, ImageParamNode, ShapeParamNode, AudioParamNode, VideoParamNode, StandardDrawingParamNode, StandardPlayingParamNode, FloatTrackBarRanges, GroupObjectParamNode
from exofile import Color, String, Float, Int, Boolean, ShapeType, TextAlignment, TrackBarType
from pathlib import Path 
from collections.abc import Iterable
from .file_utility import search_file 
from .parent_holder import ParentHolder 
from .config_holder import ConfigHolder 
from .temp_symlink import TempSymLink
from .environment_holder import EnvironmentHolder 

class Object (ParentHolder, ConfigHolder, EnvironmentHolder):

  def __init__ (self, *, parent, config, environment):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self._cachedobjnodes = None 

  @property
  @abstractmethod
  def frames (self):
    pass

  @abstractmethod
  def make_objnodes (self) -> Iterable[ObjectNode]:
    pass

  def try_make_objnodes (self):
    if self._cachedobjnodes is None:
      self._cachedobjnodes = self.make_objnodes()
    return self._cachedobjnodes

  @abstractmethod
  def is_mergeable (self, obj:"Object") -> bool:
    pass

  @abstractmethod
  def merge (self, obj:"Object") -> "Object":
    pass

class GeneratedObject (Object):

  def __init__ (self, frames, *, parent, config, environment):
    super().__init__(parent=parent, config=config, environment=environment)
    self._frames = frames

  @property
  def frames (self):
    return self._frames

class SoundObject (GeneratedObject):

  def __init__ (self, file, frames, *, parent, config, environment, volume=1.0, direction=0.0, speed=1.0, loop=False):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.file = file
    self.volume = volume
    self.direction = direction
    self.speed = speed
    self.loop = loop

  def make_objnodes (self):
    objnode = ObjectNode(audio=True)
    objnode.add_objparam(AudioParamNode(Path(self.file).absolute(), playbackspeed=self.speed * 100, loopplayback=self.loop))
    objnode.add_objparam(StandardPlayingParamNode(volume=self.volume * 100, direction=self.direction * 100))
    return [ objnode ]

class SEObject (SoundObject):

  def __init__ (self, file, frames, *, parent, config, environment, volume=1.0, direction=0.0, speed=1.0, loop=False):
    super().__init__(file, frames, parent=parent, config=config, environment=environment, volume=volume, direction=direction, speed=speed, loop=False) #loop always False.

  def is_mergeable (self, obj):
    return False

  def merge (self, obj):
    raise TypeError("{!r} has not supported .merge method.".format(self)) #error

class BGMObject (SoundObject):

  def is_mergeable (self, obj):
    return (
      isinstance(obj, BGMObject) and 
      self.file == obj.file and 
      self.volume == obj.volume and 
      self.direction == obj.direction and 
      self.speed == obj.speed and 
      self.loop == obj.loop 
    )

  def merge (self, obj):
    return BGMObject(
      self.file, 
      self.frames + obj.frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment, 
      volume=self.volume, 
      direction=self.direction, 
      speed=self.speed, 
      loop=self.loop
    )

class CharacterGraphicObject (GeneratedObject):

  def __init__ (self, file, frames, *, parent, config, environment, x=0.0, y=0.0, scale=1.0):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.file = file
    self.x = x 
    self.y = y 
    self.scale = scale 

  def make_objnodes (self):
    objnode = ObjectNode()
    objnode.add_objparam(GroupObjectParamNode(self.x, self.y, 0.0, scale=self.scale * 100.0, affectedbyupperlayer=True, range=1))
    objnode2 = ObjectNode()
    objnode2.add_objparam(ImageParamNode(Path(self.file).absolute()))
    objnode2.add_objparam(StandardDrawingParamNode(0.0, 0.0, 0.0))
    return [ objnode, objnode2 ]

  def is_mergeable (self, obj):
    return (
      isinstance(obj, CharacterGraphicObject) and 
        self.file == obj.file and 
        self.x == obj.x and 
        self.y == obj.y and 
        self.scale == obj.scale 
      )

  def merge (self, obj):
    return CharacterGraphicObject(
      self.file, 
      self.frames + obj.frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      x=self.x, 
      y=self.y, 
      scale=self.scale
    )

class ColorBackgroundObject (GeneratedObject):

  def __init__ (self, color, frames, *, parent, config, environment):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.color = color 

  def make_objnodes (self):
    objnode = ObjectNode()
    objnode.add_objparam(ShapeParamNode(ShapeType.BACKGROUND, color=self.color))
    objnode.add_objparam(StandardDrawingParamNode(0, 0, 0))
    return [ objnode ]

  def is_mergeable (self, obj):
    return (
      isinstance(obj, ColorBackgroundObject) and 
      self.color == obj.color
    )

  def merge (self, obj):
    return ColorBackgroundObject(
      self.color, 
      self.frames + obj.frames, 
      parent=self.parent, 
      config=self.config,
      environment=self.environment,
    )

class ImageBackgroundObject (GeneratedObject):

  def __init__ (self, file, frames, *, parent, config, environment, stretch=False):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.file = file
    self.stretch = stretch

  def _calculate_scale (self):
    if self.stretch:
      with TempSymLink(self.file) as tempsymlink:
        image = cv2.imread(str(tempsymlink.temppath))
        if image is None:
          raise ValueError("Could not open file {!r} with opencv.".format(self.file)) #error
        imagewidth, imageheight, _ = image.shape
        scalex = self.parent.width / imagewidth
        scaley = self.parent.height / imageheight
        return max(scalex, scaley)
    else:
      return 1.0

  def make_objnodes (self):
    scale = self._calculate_scale()
    objnode = ObjectNode()
    objnode.add_objparam(ImageParamNode(Path(self.file).absolute()))
    objnode.add_objparam(StandardDrawingParamNode(0, 0, 0, scale=scale * 100))
    return [ objnode ]

  def is_mergeable (self, obj):
    return (
      isinstance(obj, ImageBackgroundObject) and 
      self.file == obj.file and 
      self.stretch == obj.stretch
    )

  def merge (self, obj):
    return ImageBackgroundObject(
      self.file, 
      self.frames + obj.frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      stretch=self.stretch
    )

class VideoBackgroundObject (GeneratedObject):

  def __init__ (self, file, frames, *, parent, config, environment, stretch=False, loop=False):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.file = file 
    self.stretch = stretch
    self.loop = loop

  def _calculate_scale (self):
    if self.stretch:
      with TempSymLink(self.file) as tempsymlink:
        videocapture = cv2.VideoCapture(str(tempsymlink.temppath))
        if videocapture is None:
          raise ValueError("Could not open file {!r} with opencv.".format(self.file)) #error
        try:
          videocapturewidth = videocapture.get(3)
          videocaptureheight = videocapture.get(4)
          videocapture.release()
          scalex = self.parent.width / videocapturewidth
          scaley = self.parent.height / videocaptureheight
          return max(scalex, scaley)
        finally:
          videocapture.release()
    else:
      return 1.0

  def make_objnodes (self):
    scale = self._calculate_scale()
    objnode = ObjectNode()
    objnode.add_objparam(VideoParamNode(Path(self.file).absolute(), loopplayback=self.loop))
    objnode.add_objparam(StandardDrawingParamNode(0, 0, 0, scale=scale * 100))
    return [ objnode ]

  def is_mergeable (self, obj):
    return (
      isinstance(obj, ImageBackgroundObject) and 
      self.file == obj.file and 
      self.stretch == obj.stretch and 
      self.loop == obj.loop
    )

  def merge (self, obj):
    return ImageBackgroundObject(
      self.file, 
      self.frames + obj.frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      stretch=self.stretch,
      loop=self.loop
    )

class CinemaScopeObject (GeneratedObject):

  def __init__ (self, ratio, frames, *, parent, config, environment, color=Color(0, 0, 0)):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.ratio = ratio
    self.color = color 

  def make_objnodes (self):
    height = self.parent.height * (1.0 / self.ratio)
    objnode = ObjectNode()
    objnode.add_objparam(ShapeParamNode(ShapeType.BACKGROUND, color=self.color))
    objnode.add_objparam(StandardDrawingParamNode(0, 0, 0))
    objnode.add_objparam(ObjectParamNode(**{ 
      "_name": "斜めクリッピング", 
      "中心X": 0, 
      "中心Y": 0, 
      "角度": 0.0, 
      "ぼかし": 0, 
      "幅": -height 
    }))
    return [ objnode ]

  def is_mergeable (self, obj):
    return (
      isinstance(obj, CinemaScopeObject) and 
      self.ratio == obj.ratio and 
      self.color == obj.color
    )

  def merge (self, obj):
    return CinemaScopeObject(
      self.ratio, 
      self.frames + obj.frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      color=self.color
    )

class SubtitleObject (GeneratedObject):

  def __init__ (self, text, frames, *, parent, config, environment, x=0, y=0, font="Meiryo", size=30, color=Color(255, 255, 255)):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.text = text
    self.x = x
    self.y = y
    self.font = font 
    self.size = size
    self.color = color 

  def make_objnodes (self):
    objnode = ObjectNode()
    objnode.add_objparam(TextParamNode(self.text, font=self.font, size=self.size, color=self.color, align=TextAlignment.ALIGN_CENTER_MIDDLE))
    objnode.add_objparam(StandardDrawingParamNode(self.x, self.y, 0))
    return [ objnode ]

  def is_mergeable (self, obj):
    return (
      isinstance(obj, SubtitleObject) and 
      self.text == obj.text and 
      self.x == obj.x and 
      self.y == obj.y and 
      self.font == obj.font and 
      self.size == obj.size and 
      self.color == obj.color 
    )

  def merge (self, obj):
    return SubtitleObject(
      self.text, 
      self.frames + obj.frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      x=self.x, 
      y=self.y, 
      font=self.font, 
      size=self.size, 
      color=self.color
    )
 
class FilterObject (Object):

  def __init__ (self, obj, *, parent, config, environment):
    super().__init__(parent=parent, config=config, environment=environment)
    self._object = obj 

  @property
  def object (self):
    return self._object

  @property
  def rootobject (self):
    obj = self 
    while isinstance(obj, FilterObject):
      obj = obj.object
    return obj 

  @property
  def frames (self):
    return self._object.frames

class BounceObject (FilterObject):

  def __init__ (self, obj, *, parent, config, environment, crashratio=1.05, interval=0.5):
    super().__init__(obj, parent=parent, config=config, environment=environment)
    self.crashratio = crashratio
    self.interval = interval

  def make_objnodes (self):
    objnodes = self.object.try_make_objnodes()
    objnode = ObjectNode()
    objnode.add_objparam(GroupObjectParamNode(0.0, 0.0, 0.0, affectedbyupperlayer=True, range=len(objnodes)))
    scalex = self.crashratio
    scaley = 1.0 + 1.0 - self.crashratio 
    objnode.add_objparam(ObjectParamNode(**{
      "_name": "拡大率",
      "拡大率": Float(100.0, decimalpartdigits=2),
      "X": FloatTrackBarRanges((Float(100.0, decimalpartdigits=2), Float(scalex * 100.0, decimalpartdigits=2)), TrackBarType.REPETITION, accelerate=False, decelerate=False, parameter=Int(self.interval / 2.0 * self.parent.framerate)),
      "Y": FloatTrackBarRanges((Float(100.0, decimalpartdigits=2), Float(scaley * 100.0, decimalpartdigits=2)), TrackBarType.REPETITION, accelerate=False, decelerate=False, parameter=Int(self.interval / 2.0 * self.parent.framerate)),
    }))
    return [ objnode ] + objnodes

  def is_mergeable (self, obj):
    return (
      isinstance(obj, BounceObject) and 
      self.object.is_mergeable(obj.object) and 
      self.crashratio == obj.crashratio and 
      self.interval == obj.interval 
    )

  def merge (self, obj):
    return BounceObject(
      self.object.merge(obj.object), 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      crashratio=self.crashratio,
      interval=self.interval
    )

class HoppingObject (FilterObject):

  def __init__ (self, obj, *, parent, config, environment, crashratio=1.05, height=100, interval=1.0):
    super().__init__(obj, parent=parent, config=config, environment=environment)
    self.crashratio = crashratio
    self.height = height
    self.interval = interval

  def make_objnodes (self):
    objnodes = self.object.try_make_objnodes()
    objnode = ObjectNode()
    objnode.add_objparam(GroupObjectParamNode(0.0, 0.0, 0.0, affectedbyupperlayer=True, range=len(objnodes)))
    objnode.add_objparam(ObjectParamNode(**{
      "_name": "アニメーション効果",
      "track0": Float(1.0 / self.interval * 10.0, decimalpartdigits=2),
      "track1": Float(self.height, decimalpartdigits=2),
      "track2": Float(0.0, decimalpartdigits=2),
      "track3": Float(0.0, decimalpartdigits=2),
      "type": Int(2), #弾む
      "filter": Boolean(False), #0
      "name": String(""), 
      "param": String(""), 
    }))
    scalex = self.crashratio
    scaley = 1.0 + 1.0 - self.crashratio
    objnode.add_objparam(ObjectParamNode(**{
      "_name": "拡大率",
      "拡大率": Float(100.0, decimalpartdigits=2),
      "X": FloatTrackBarRanges((Float(scalex * 100.0, decimalpartdigits=2), Float(100.0, decimalpartdigits=2)), TrackBarType.REPETITION, accelerate=False, decelerate=False, parameter=Int(self.interval / 2.0 * self.parent.framerate)),
      "Y": FloatTrackBarRanges((Float(scaley * 100.0, decimalpartdigits=2), Float(100.0, decimalpartdigits=2)), TrackBarType.REPETITION, accelerate=False, decelerate=False, parameter=Int(self.interval / 2.0 * self.parent.framerate)),
    }))
    return [ objnode ] + objnodes

  def is_mergeable (self, obj):
    return (
      isinstance(obj, RasterObject) and 
      self.object.is_mergeable(obj.object) and 
      self.crashratio == obj.crashratio and 
      self.height == obj.height and 
      self.interval == obj.interval 
    )

  def merge (self, obj):
    return RasterObject(
      self.object.merge(obj.object), 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      crashratio=self.crashratio,
      height=self.height, 
      interval=self.interval
    )

class RasterObject (FilterObject):

  def __init__ (self, obj, *, parent, config, environment, width=100, height=100, interval=1.0):
    super().__init__(obj, parent=parent, config=config, environment=environment)
    self.width = width
    self.height = height
    self.interval = interval

  def make_objnodes (self):
    objnodes = self.object.try_make_objnodes()
    objnode = ObjectNode()
    objnode.add_objparam(GroupObjectParamNode(0.0, 0.0, 0.0, affectedbyupperlayer=True, range=len(objnodes)))
    objnode.add_objparam(ObjectParamNode(**{
      "_name": "ラスター",
      "横幅": Int(self.width),
      "高さ": Int(self.height),
      "周期": Float(self.interval),
      "縦ラスター": Boolean(False),
      "ランダム振幅": Boolean(False),
    }))
    return [ objnode ] + objnodes

  def is_mergeable (self, obj):
    return (
      isinstance(obj, RasterObject) and 
      self.object.is_mergeable(obj.object) and 
      self.width == obj.width and 
      self.height == obj.height and 
      self.interval == obj.interval 
    )

  def merge (self, obj):
    return RasterObject(
      self.object.merge(obj.object), 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      width=self.width, 
      height=self.height, 
      interval=self.interval
    )
