
from exolib import ObjectNode, TextParamNode, CustomObjectParamNode, AnimationEffectObjectParamNode, StandardDrawingParamNode, ObjectParamNode, GroupObjectParamNode
from exofile import String, Float, Int, Boolean, ParamString, Param
from pathlib import Path 
from psd_tools import PSDImage
from collections import OrderedDict
from psdtoolkit_util import Flip, PSDVisibles, Params as PSDParams 
from .object import SoundObject, FilterObject, GeneratedObject

class PSDToolKitLipSyncPreparationObject_0_1_3 (FilterObject):

  def __init__ (self, obj, *, parent, config, environment, lowcut=100, highcut=1000, threshold=0.333):
    super().__init__(obj, parent=parent, config=config, environment=environment)
    self.lowcut = lowcut
    self.highcut = highcut
    self.threshold = threshold

  def make_objnodes (self):
    rootobj = self.rootobject
    if isinstance(rootobj, SoundObject):
      objnode = ObjectNode()
      objnode.add_objparam(CustomObjectParamNode(
        "口パク準備@PSDToolKit", 
        self.lowcut, 
        self.highcut, 
        round(self.threshold * self.parent.framerate), 
        filter=2, 
        param=Param({ 
          "file": ParamString(Path(rootobj.file).absolute()),
        })
      ))
      return [ objnode ] + self.object.make_objnodes()
    else:
      return self.object.make_objnodes()

  def is_mergeable (self, obj):
    return (
      isinstance(obj, PSDToolKitLipSyncPreparationObject_0_1_3) and 
      self.object.is_mergeable(obj.object) and 
      self.lowcut == obj.lowcut and 
      self.highcut == obj.highcut and 
      self.threshold == obj.threshold 
    )

  def merge (self, obj):
    return PSDToolKitLipSyncPreparationObject_0_1_3(
      self.object.merge(obj.object), 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      lowcut=self.lowcut,
      highcut=self.highcut,
      threshold=self.threshold
    )

class PSDToolKitObject_0_1_3 (GeneratedObject):

  def __init__ (self, file, frames, *, parent, config, environment, encoding="cp932", x=0.0, y=0.0, scale=1.0, flip=Flip.NONE, psdvisibles=PSDVisibles(), nowspeaking=False, blinker=None, lipsyncer=None):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.file = file
    self.encoding = encoding
    self.x = x 
    self.y = y 
    self.scale = scale 
    self.flip = Flip(flip)
    self.psdvisibles = psdvisibles
    self.nowspeaking = nowspeaking
    self.blinker = blinker
    self.lipsyncer = lipsyncer

  def make_objnodes (self):
    objnode = ObjectNode()
    objnode.add_objparam(GroupObjectParamNode(self.x, self.y, 0.0, scale=self.scale * 100.0, affectedbyupperlayer=True, range=1))
    objnode2 = ObjectNode()
    objnode2.add_objparam(TextParamNode(Path(self.file).name))
    objnode2.add_objparam(StandardDrawingParamNode(0.0, 0.0, 0.0))
    objnode2.add_objparam(AnimationEffectObjectParamNode(
      "Assign@PSDToolKit",
      0.0,
      100.0,
      0.0,
      0.0,
      check0=False,
      filter=2,
      param=Param({
        "f": ParamString(Path(self.file).absolute()),
        "l": ParamString(PSDParams({
          "L.": self.flip,
          "V.": self.psdvisibles,
        }).serialize()),
      })
    ))
    if self.blinker:
      self.blinker.apply_objnode(objnode2, self.nowspeaking)
    if self.lipsyncer:
      self.lipsyncer.apply_objnode(objnode2, self.nowspeaking)
    objnode2.add_objparam(AnimationEffectObjectParamNode(
      "オブジェクト描画@PSDToolKit",
      filter=2
    ))
    return [ objnode, objnode2 ]

  def is_mergeable (self, obj):
    return (
      isinstance(obj, PSDToolKitObject_0_1_3) and 
      self.file == obj.file and 
      self.encoding == obj.encoding and 
      self.x == obj.x and 
      self.y == obj.y and 
      self.scale == obj.scale and  
      self.flip == obj.flip and 
      self.psdvisibles == obj.psdvisibles and 
      self.nowspeaking == obj.nowspeaking and 
      self.blinker == obj.blinker and 
      self.lipsyncer == obj.lipsyncer
    )

  def merge (self, obj):
    return PSDToolKitObject_0_1_3(
      self.file, 
      self.frames + obj.frames, 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      encoding=self.encoding,
      x=self.x, 
      y=self.y, 
      scale=self.scale,
      flip=self.flip,
      psdvisibles=self.psdvisibles,
      nowspeaking=self.nowspeaking,
      blinker=self.blinker,
      lipsyncer=self.lipsyncer
    )
