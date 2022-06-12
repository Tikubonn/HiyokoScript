
from exolib import AnimationEffectObjectParamNode, ObjectParamNode
from exofile import String, Float, Int, Boolean, ParamString, Param
from pathlib import Path 
from psdtoolkit_util import Flip, PSDVisibles, Params as PSDParams
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .speaker_graphic import SpeakerGraphic
from .psdtoolkit_object_0_1_3 import PSDToolKitObject_0_1_3
from .file_utility import search_file
from .environment_holder import EnvironmentHolder 

class Blinker (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  def __init__ (self, file, *, parent, config, environment, encoding="cp932", flip=Flip.NONE, layervisibles={}, interval=2.0, speed=1, offset=0, m0layervisibles={}, m1layervisibles={}, m2layervisibles={}, m3layervisibles={}, m4layervisibles={}):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self.file = file
    self.encoding = encoding
    self.interval = interval
    self.speed = speed
    self.offset = offset
    self.flip = Flip(flip)
    self.layervisibles = layervisibles
    self.m0layervisibles = m0layervisibles
    self.m1layervisibles = m1layervisibles
    self.m2layervisibles = m2layervisibles
    self.m3layervisibles = m3layervisibles
    self.m4layervisibles = m4layervisibles
    self.m0psdvisibles = None 
    self.m1psdvisibles = None 
    self.m2psdvisibles = None 
    self.m3psdvisibles = None 
    self.m4psdvisibles = None 

  def make_psdvisibles (self, mlayervisibles):
    foundfile = search_file(self.file, config=self.config, environment=self.environment)
    psdvisibles = PSDVisibles.open(Path(foundfile).absolute(), encoding=self.encoding)
    for path, visible in self.layervisibles.items():
      psdvisibles.change_visible(path, visible)
    for path, visible in mlayervisibles.items():
      psdvisibles.change_visible(path, visible)
    return psdvisibles

  def prepare_all_psdvisibles (self, *, reload=False):
    if self.m0psdvisibles is None or reload:
      self.m0psdvisibles = self.make_psdvisibles(self.m0layervisibles)
    if self.m1psdvisibles is None or reload:
      self.m1psdvisibles = self.make_psdvisibles(self.m1layervisibles)
    if self.m2psdvisibles is None or reload:
      self.m2psdvisibles = self.make_psdvisibles(self.m2layervisibles)
    if self.m3psdvisibles is None or reload:
      self.m3psdvisibles = self.make_psdvisibles(self.m3layervisibles)
    if self.m4psdvisibles is None or reload:
      self.m4psdvisibles = self.make_psdvisibles(self.m4layervisibles)
    return self.m0psdvisibles, self.m1psdvisibles, self.m2psdvisibles, self.m3psdvisibles, self.m4psdvisibles

  def apply_objnode (self, objnode, nowspeaking=False):
    m0lvisibles, m1lvisibles, m2lvisibles, m3lvisibles, m4lvisibles = self.prepare_all_psdvisibles()
    objnode.add_objparam(AnimationEffectObjectParamNode(
      "目パチ@PSDToolKit",
      self.interval * self.parent.framerate,
      self.speed,
      self.offset,
      param=Param({
        "m0": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m0lvisibles,
        }).serialize()),
        "m1": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m1lvisibles,
        }).serialize()),
        "m2": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m2lvisibles,
        }).serialize()),
        "m3": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m3lvisibles,
        }).serialize()),
        "m4": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m4lvisibles,
        }).serialize()),
      }),
    ))

  @classmethod
  def deserialize (cls, params, file, *, parent, config, environment, encoding="cp932", flip=Flip.NONE, layervisibles={}):
    return cls(
      file,
      parent=parent,
      config=config,
      environment=environment,
      encoding=encoding,
      interval=params.get("interval", 2.0), 
      speed=params.get("speed", 1), 
      offset=params.get("offset", 0), 
      flip=flip,
      layervisibles=layervisibles,
      m0layervisibles=params.get("m0", {}),
      m1layervisibles=params.get("m1", {}),
      m2layervisibles=params.get("m2", {}),
      m3layervisibles=params.get("m3", {}),
      m4layervisibles=params.get("m4", {}),
    )

class LipSyncer (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  def __init__ (self, file, *, parent, config, environment, encoding="cp932", flip=Flip.NONE, layervisibles={}, speed=1, referencelayer=0, m0layervisibles={}, m1layervisibles={}, m2layervisibles={}, m3layervisibles={}, m4layervisibles={}):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self.file = file
    self.encoding = encoding
    self.speed = speed
    self.referencelayer = referencelayer
    self.flip = Flip(flip)
    self.layervisibles = layervisibles
    self.m0layervisibles = m0layervisibles
    self.m1layervisibles = m1layervisibles
    self.m2layervisibles = m2layervisibles
    self.m3layervisibles = m3layervisibles
    self.m4layervisibles = m4layervisibles
    self.m0psdvisibles = None
    self.m1psdvisibles = None
    self.m2psdvisibles = None
    self.m3psdvisibles = None
    self.m4psdvisibles = None

  def make_psdvisibles (self, mlayervisibles):
    foundfile = search_file(self.file, config=self.config, environment=self.environment)
    psdvisibles = PSDVisibles.open(Path(foundfile).absolute(), encoding=self.encoding)
    for path, visible in self.layervisibles.items():
      psdvisibles.change_visible(path, visible)
    for path, visible in mlayervisibles.items():
      psdvisibles.change_visible(path, visible)
    return psdvisibles

  def prepare_all_psdvisibles (self, *, reload=False):
    if self.m0psdvisibles is None or reload:
      self.m0psdvisibles = self.make_psdvisibles(self.m0layervisibles)
    if self.m1psdvisibles is None or reload:
      self.m1psdvisibles = self.make_psdvisibles(self.m1layervisibles)
    if self.m2psdvisibles is None or reload:
      self.m2psdvisibles = self.make_psdvisibles(self.m2layervisibles)
    if self.m3psdvisibles is None or reload:
      self.m3psdvisibles = self.make_psdvisibles(self.m3layervisibles)
    if self.m4psdvisibles is None or reload:
      self.m4psdvisibles = self.make_psdvisibles(self.m4layervisibles)
    return self.m0psdvisibles, self.m1psdvisibles, self.m2psdvisibles, self.m3psdvisibles, self.m4psdvisibles

  def apply_objnode (self, objnode, nowspeaking=False):
    m0lvisibles, m1lvisibles, m2lvisibles, m3lvisibles, m4lvisibles = self.prepare_all_psdvisibles()
    objnode.add_objparam(AnimationEffectObjectParamNode(
      "口パク 開閉のみ@PSDToolKit",
      self.speed,
      0.0,
      0.0,
      self.referencelayer,
      param=Param({
        "m0": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m0lvisibles,
        }).serialize()),
        "m1": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m1lvisibles,
        }).serialize()),
        "m2": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m2lvisibles,
        }).serialize()),
        "m3": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m3lvisibles,
        }).serialize()),
        "m4": ParamString(PSDParams({
          "L.": self.flip,
          "V.": m4lvisibles,
        }).serialize()),
      }),
      _disable=Boolean(not nowspeaking),
    ))

  @classmethod
  def deserialize (cls, params, file, *, parent, config, environment, encoding="cp932", flip=Flip.NONE, layervisibles={}):
    return cls(
      file,
      parent=parent,
      config=config,
      environment=environment,
      encoding=encoding,
      speed=params.get("speed", 1), 
      referencelayer=params.get("reference_layer", 0), 
      flip=flip,
      layervisibles=layervisibles,
      m0layervisibles=params.get("m0", {}),
      m1layervisibles=params.get("m1", {}),
      m2layervisibles=params.get("m2", {}),
      m3layervisibles=params.get("m3", {}),
      m4layervisibles=params.get("m4", {}),
    )

class PSDToolKitSpeakerGraphic_0_1_3 (SpeakerGraphic):

  def __init__ (self, file, *, parent, config, environment, default=False, encoding="cp932", x=0.0, y=0.0, scale=1.0, flip=Flip.NONE, layervisibles={}, blinker=None, lipsyncer=None):
    super().__init__(parent=parent, config=config, environment=environment, default=default)
    self.file = file 
    self.encoding = encoding
    self.x = x
    self.y = y 
    self.scale = scale
    self.flip = Flip(flip)
    self.layervisibles = layervisibles
    self.psdvisibles = None 
    self.blinker = blinker
    self.lipsyncer = lipsyncer

  def make_psdvisibles (self):
    foundfile = search_file(self.file, config=self.config, environment=self.environment)
    psdvisibles = PSDVisibles.open(Path(foundfile).absolute(), encoding=self.encoding)
    for path, visible in self.layervisibles.items():
      psdvisibles.change_visible(path, visible)
    return psdvisibles

  def prepare_psdvisibles (self, *, reload=False):
    if self.psdvisibles is None or reload:
      self.psdvisibles = self.make_psdvisibles()
    return self.psdvisibles

  def make_object (self, x, y, frames):
    foundfile = search_file(self.file, config=self.config, environment=self.environment)
    psdvisibles = self.prepare_psdvisibles()
    return PSDToolKitObject_0_1_3(
      Path(foundfile).absolute(), 
      frames,
      encoding=self.encoding,
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      x=self.x + x, 
      y=self.y + y, 
      scale=self.scale, 
      flip=self.flip,
      psdvisibles=psdvisibles,
      nowspeaking=self.parent.now_speaking_graphic(self),
      blinker=self.blinker,
      lipsyncer=self.lipsyncer,
    )

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    flip = Flip.NONE
    flip = flip.flip_x(params.get("flip_x", False))
    flip = flip.flip_y(params.get("flip_y", False))
    layervisibles = params.get("layer_visibles", {})
    if "blink" in params:
      blinker = Blinker.deserialize(
        params["blink"],
        params["src"],
        parent=parent,
        config=config,
        environment=environment,
        encoding=params.get("encoding", "cp932"),
        flip=flip,
        layervisibles=layervisibles,
      )
    else:
      blinker = None 
    if "lipsync" in params:
      lipsyncer = LipSyncer.deserialize(
        params["lipsync"],
        params["src"],
        parent=parent,
        config=config,
        environment=environment,
        encoding=params.get("encoding", "cp932"),
        flip=flip,
        layervisibles=layervisibles,
      )
    else:
      lipsyncer = None 
    return cls(
      params["src"],
      parent=parent,
      config=config,
      environment=environment,
      default=params.get("default", False),
      encoding=params.get("encoding", "cp932"),
      x=params.get("x", 0.0),
      y=params.get("y", 0.0),
      scale=params.get("scale", 1.0),
      flip=flip,
      layervisibles=layervisibles,
      blinker=blinker,
      lipsyncer=lipsyncer,
    )
