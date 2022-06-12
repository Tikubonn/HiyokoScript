
from exolib import ObjectNode, TextParamNode, StandardDrawingParamNode, CustomObjectParamNode, AnimationEffectObjectParamNode, GroupObjectParamNode
from exofile import ParamString, Param
from pathlib import Path 
from psdtoolkit_util import Flip, PSDVisibles, Params as PSDParams
from .object import FilterObject, GeneratedObject, SoundObject

class PSDToolKitLipSyncPreparationObject_0_2 (FilterObject):

  def __init__ (self, obj, *, parent, config, environment, lowcut=0, highcut=0, threshold=0, sensitivity=0):
    super().__init__(obj, parent=parent, config=config, environment=environment)
    self.lowcut = lowcut
    self.highcut = highcut
    self.threshold = threshold
    self.sensitivity = sensitivity

  def make_objnodes (self):
    rootobj = self.rootobject
    if isinstance(rootobj, SoundObject):
      objnode = ObjectNode()
      objnode.add_objparam(CustomObjectParamNode(
        "口パク準備@PSDToolKit",
        self.lowcut,
        self.highcut,
        self.threshold,
        self.sensitivity,
        filter=2,
        param=Param({
          "file": ParamString(Path(rootobj.file).absolute()),
        }),
      ))
      return [ objnode ] + self.object.make_objnodes()
    else:
      return self.object.make_objnodes()

  def is_mergeable (self, obj):
    return (
      isinstance(obj, PSDToolKitLipSyncPreparationObject_0_2) and 
      self.object.is_mergeable(obj.object) and 
      self.lowcut == obj.lowcut and 
      self.highcut == obj.highcut and 
      self.threshold == obj.threshold 
    )

  def merge (self, obj):
    return PSDToolKitLipSyncPreparationObject_0_2(
      self.object.merge(obj.object), 
      parent=self.parent, 
      config=self.config, 
      environment=self.environment,
      lowcut=self.lowcut,
      highcut=self.highcut,
      threshold=self.threshold
    )

class PSDToolKitObject_0_2 (GeneratedObject):

  SCRIPT_TEMPLATE = """
<?-- {filename:s}

o={{ -- オプション設定
lipsync = {lipsync_layer:d}    ,-- 口パク準備のレイヤー番号
mpslider = 0    ,-- 多目的スライダーのレイヤー番号
scene = 0    ,-- シーン番号
tag = {tag:d}    ,-- 識別用タグ

-- 口パク準備のデフォルト設定
ls_locut = {low_cut:d}    ,-- ローカット
ls_hicut = {high_cut:d}    ,-- ハイカット
ls_threshold = {threshold:d}    ,-- しきい値
ls_sensitivity = {sensitivity:d}    ,-- 感度

-- 以下は書き換えないでください
ptkf="{file:s}",ptkl="{param:s}"}}PSD,subobj=require("PSDToolKit").PSDState.init(obj,o)?>
"""

  def __init__ (self, file, frames, *, parent, config, environment, encoding="cp932", x=0.0, y=0.0, scale=1.0, flip=Flip.NONE, psdvisibles=PSDVisibles(), nowspeaking=False, blinker=None, lipsyncer=None, tag=0):
    super().__init__(frames, parent=parent, config=config, environment=environment)
    self.file = file
    self.encoding = encoding
    self.x = x 
    self.y = y 
    self.scale = scale 
    self.flip = Flip(flip)
    self.psdvisibles = psdvisibles
    self.scriptcode = None 
    self.nowspeaking = nowspeaking
    self.blinker = blinker
    self.lipsyncer = lipsyncer
    self.tag = tag

  def make_script_code (self):
    if self.lipsyncer:
      lowcut = self.lipsyncer.lowcut
      highcut = self.lipsyncer.highcut
      threshold = self.lipsyncer.threshold
      sensitivity = self.lipsyncer.sensitivity
      #lipsynclayer = self.lipsyncer.referencelayer
      lipsynclayer = self.lipsyncer.referencelayer if self.nowspeaking else 0
    else:
      lowcut = 100
      highcut = 1000
      threshold = 20
      sensitivity = 1
      lipsynclayer = 0
    return self.SCRIPT_TEMPLATE.strip().format(
      filename=str(Path(self.file).name),
      tag=self.tag,
      low_cut=lowcut,
      high_cut=highcut,
      threshold=threshold,
      sensitivity=sensitivity,
      lipsync_layer=lipsynclayer,
      file=str(Path(self.file).absolute()).replace("\\", "\\\\"),
      param=PSDParams({
        "L.": self.flip,
        "V.": self.psdvisibles,
      }).serialize(),
    )

  def prepare_script_code (self):
    if self.scriptcode is None:
      self.scriptcode = self.make_script_code()
    return self.scriptcode

  def make_objnodes (self):
    objnode = ObjectNode()
    objnode.add_objparam(GroupObjectParamNode(self.x, self.y, 0.0, scale=self.scale * 100.0, affectedbyupperlayer=True, range=1))
    scriptcode = self.prepare_script_code()
    objnode2 = ObjectNode()
    objnode2.add_objparam(TextParamNode(scriptcode, size=1)) 
    objnode2.add_objparam(StandardDrawingParamNode(0.0, 0.0, 0.0))
    if self.blinker:
      self.blinker.apply_objnode(objnode2, self.nowspeaking)
    if self.lipsyncer:
      self.lipsyncer.apply_objnode(objnode2, self.nowspeaking)
    objnode2.add_objparam(AnimationEffectObjectParamNode("描画@PSD", -1, 100.0, 0, 0, filter=2))
    return [ objnode, objnode2 ]

  def is_mergeable (self, obj):
    return (
      isinstance(obj, PSDToolKitObject_0_2) and 
      self.file == obj.file and 
      self.encoding == obj.encoding and 
      self.x == obj.x and 
      self.y == obj.y and 
      self.scale == obj.scale and  
      self.flip == obj.flip and 
      self.psdvisibles == obj.psdvisibles and 
      self.nowspeaking == obj.nowspeaking and 
      self.blinker == obj.blinker and 
      self.lipsyncer == obj.lipsyncer and 
      self.tag == obj.tag
    )

  def merge (self, obj):
    return PSDToolKitObject_0_2(
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
      lipsyncer=self.lipsyncer,
      tag=self.tag,
    )
