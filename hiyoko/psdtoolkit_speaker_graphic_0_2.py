
from exolib import AnimationEffectObjectParamNode
from exofile import ParamString, Param, Boolean
from pathlib import Path 
from hashlib import md5
from psdtoolkit_util import Flip, PSDVisibles
from .file_utility import search_file
from .parent_holder import ParentHolder
from .config_holder import ConfigHolder
from .deserializable import Deserializable
from .speaker_graphic import SpeakerGraphic
from .psdtoolkit_object_0_2 import PSDToolKitObject_0_2
from .environment_holder import EnvironmentHolder 

class Blinker (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  def __init__ (self, *, parent, config, environment, interval=4.0, speed=1, offset=0, alayer="", blayer="", clayer="", dlayer="", elayer=""):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self.interval = interval
    self.speed = speed
    self.offset = offset
    self.alayer = alayer
    self.blayer = blayer
    self.clayer = clayer
    self.dlayer = dlayer
    self.elayer = elayer

  def apply_objnode (self, objnode, nowspeaking=False):
    objnode.add_objparam(AnimationEffectObjectParamNode(
      "目パチ@PSD",
      self.interval,
      self.speed,
      self.offset,
      param=Param({
        "a": ParamString(self.alayer and ("v1." + self.alayer)),
        "b": ParamString(self.blayer and ("v1." + self.blayer)),
        "c": ParamString(self.clayer and ("v1." + self.clayer)),
        "d": ParamString(self.dlayer and ("v1." + self.dlayer)),
        "e": ParamString(self.elayer and ("v1." + self.elayer)),
      }),
      _disable=Boolean(not self.alayer or not self.elayer), #閉じる・開くが未指定ならば無効化します。
    ))

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent,
      config=config,
      environment=environment,
      interval=params.get("interval", 4.0), 
      speed=params.get("speed", 1), 
      offset=params.get("offset", 0), 
      alayer=params.get("a", ""),
      blayer=params.get("b", ""),
      clayer=params.get("c", ""),
      dlayer=params.get("d", ""),
      elayer=params.get("e", ""),
    )

class LipSyncer (ParentHolder, ConfigHolder, EnvironmentHolder, Deserializable):

  def __init__ (self, *, parent, config, environment, speed=1, lowcut=100, highcut=1000, threshold=20, sensitivity=1, referencelayer=0, alayer="", blayer="", clayer="", dlayer="", elayer=""):
    ParentHolder.__init__(self, parent=parent)
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self.speed = speed
    self.lowcut = lowcut #referred from outside.
    self.highcut = highcut #referred from outside.
    self.threshold = threshold #referred from outside.
    self.sensitivity = sensitivity #referred from outside.
    self.referencelayer = referencelayer #referred from outside.
    self.alayer = alayer
    self.blayer = blayer
    self.clayer = clayer
    self.dlayer = dlayer
    self.elayer = elayer

  def apply_objnode (self, objnode, nowspeaking=False):
    objnode.add_objparam(AnimationEffectObjectParamNode(
      "パーツ差し替え@PSD",
      1,
      param=Param({
        "a": ParamString(self.alayer and ("v1." + self.elayer)),
      }),
      _disable=Boolean(not self.alayer or not self.elayer), #tmp
    ))
    objnode.add_objparam(AnimationEffectObjectParamNode(
      "口パク 開閉のみ@PSD",
      self.speed,
      param=Param({
        "a": ParamString(self.alayer and ("v1." + self.alayer)),
        "b": ParamString(self.blayer and ("v1." + self.blayer)),
        "c": ParamString(self.clayer and ("v1." + self.clayer)),
        "d": ParamString(self.dlayer and ("v1." + self.dlayer)),
        "e": ParamString(self.elayer and ("v1." + self.elayer)),
      }),
      _disable=Boolean(not nowspeaking or not self.alayer or not self.elayer), #沈黙あるいは閉じる・開くが未指定ならば無効化します。
    ))

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent,
      config=config,
      environment=environment,
      speed=params.get("speed", 1), 
      lowcut=params.get("low_cut", 100),
      highcut=params.get("high_cut", 1000),
      threshold=params.get("threshold", 20),
      sensitivity=params.get("sensitivity", 1),
      referencelayer=params.get("reference_layer", 0),
      alayer=params.get("a", ""),
      blayer=params.get("b", ""),
      clayer=params.get("c", ""),
      dlayer=params.get("d", ""),
      elayer=params.get("e", ""),
    )

class PSDToolKitSpeakerGraphic_0_2 (SpeakerGraphic):

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
    return PSDToolKitObject_0_2(
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
      tag=int.from_bytes(md5(str(Path(foundfile).absolute()).encode("utf-8")).digest()[:4], "little"), #tmp
    )

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    flip = Flip.NONE
    flip = flip.flip_x(params.get("flip_x", False))
    flip = flip.flip_y(params.get("flip_y", False))
    if "blink" in params:
      blinker = Blinker.deserialize(
        params["blink"],
        parent=parent,
        config=config,
        environment=environment,
      )
    else:
      blinker = None 
    if "lipsync" in params:
      lipsyncer = LipSyncer.deserialize(
        params["lipsync"],
        parent=parent,
        config=config,
        environment=environment,
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
      layervisibles=params.get("layer_visibles", {}),
      blinker=blinker,
      lipsyncer=lipsyncer,
    )
