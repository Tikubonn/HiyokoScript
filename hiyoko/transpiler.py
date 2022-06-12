
import math 
from exolib import EXO 
from ordered_set import OrderedSet
from .speaker import Speaker
from .variables import Variables
from .layer_group import LayerGroup
from .config_holder import ConfigHolder 
from .deserializable import Deserializable
from .speaker_voice_generator import SpeakerVoiceGenerator
from .speaker_graphic_generator import SpeakerGraphicGenerator
from .speaker_voice_postprocessor import SpeakerVoicePostProcessor
from .speaker_graphic_postprocessor import SpeakerGraphicPostProcessor
from .object_generator import ObjectGenerator
from .environment_holder import EnvironmentHolder

class Transpiler (ConfigHolder, EnvironmentHolder, Deserializable):

  syntax_processor_types = []

  def __init__ (self, *, width=1280, height=720, framerate=24, scale=1, audiorate=44100, audioch=2, config, environment):
    ConfigHolder.__init__(self, config=config)
    EnvironmentHolder.__init__(self, environment=environment)
    self._syntaxprocessors = [ syntaxprocessor(self) for syntaxprocessor in self.syntax_processor_types ]
    self._width = width 
    self._height = height 
    self._framerate = framerate 
    self._scale = scale 
    self._audiorate = audiorate 
    self._audioch = audioch
    self._speakervoicegenerator = None 
    self._speakergraphicgenerator = None 
    self._speakervoicepostprocessors = list() 
    self._speakergraphicpostprocessors = list() 
    self._foregroundobjectgenerators = list()
    self._backgroundobjectgenerators = list()
    self._textpostprocessors = list()
    self._speakers = dict()
    self.curspeakers = OrderedSet()
    self.curspeakervoices = OrderedSet()
    self.variables = Variables()
    self._speakervoicelayergroup = LayerGroup()
    self._speakergraphiclayergroup = LayerGroup()
    self._foregroundlayergroup = LayerGroup()
    self._backgroundlayergroup = LayerGroup()
    self._offset = 1

  @property
  def width (self):
    return self._width

  @property
  def height (self):
    return self._height

  @property
  def framerate (self):
    return self._framerate

  @property
  def scale (self):
    return self._scale

  @property
  def audiorate (self):
    return self._audiorate

  @property
  def audioch (self):
    return self._audioch

  def add_speaker (self, name, speaker):
    self._speakers[name] = speaker

  @property
  def speakers (self):
    return self._speakers.copy()
  
  @property
  def speakervoices (self):
    speakervoices = dict()
    for speaker in self._speakers.values():
      speakervoices.update(speaker.speakervoices)
    return speakervoices

  def now_speaking (self, speaker):
    for speakervoice in self.curspeakervoices:
      if speakervoice in speaker.speakervoices.values():
        return True 
    else:
      return False

  def now_speaking_graphic (self, speakergraphic):
    for speakervoice in self.curspeakervoices:
      if speakergraphic == speakervoice.graphic:
        return True 
    else:
      return False

  def set_speaker_voice_generator (self, generator):
    self._speakervoicegenerator = generator

  def set_speaker_graphic_generator (self, generator):
    self._speakergraphicgenerator = generator

  def add_speaker_voice_postprocessor (self, postprocessor):
    self._speakervoicepostprocessors.append(postprocessor)

  def add_speaker_graphic_postprocessor (self, postprocessor):
    self._speakergraphicpostprocessors.append(postprocessor)

  def add_foreground_object_generator (self, generator):
    self._foregroundobjectgenerators.append(generator)

  def add_background_object_generator (self, generator):
    self._backgroundobjectgenerators.append(generator)

  def _feed_line (self, line):
    li = line 
    while li.strip():
      li = li.strip() #tmp
      for syntaxprocessor in self._syntaxprocessors:
        status, remainder = syntaxprocessor.process(li)
        if status:
          li = remainder.strip()
          break
      else:
        break
    if li.strip():
      li = li.strip()
      self._push_section(li)

  def _push_section (self, line):
    speakervoiceobjs = list()
    speakergraphicobjs = list()
    foregroundobjs = list()
    backgroundobjs = list()
    for curspeakervoice in self.curspeakervoices:
      if self._speakervoicegenerator:
        obj = self._speakervoicegenerator.make_object(line, curspeakervoice)
        if obj:
          for postprocessor in self._speakervoicepostprocessors:
            obj = postprocessor.postprocess(line, obj, curspeakervoice)
          speakervoiceobjs.append(obj)
      else:
        raise ValueError("{!r}._speakervoicegenerator is None.".format(self)) #error 
    for generator in self._foregroundobjectgenerators:
      if generator.to_base_length:
        obj = generator.make_object(line, 0)
      else:
        obj = None 
      foregroundobjs.append(obj)
    for generator in self._backgroundobjectgenerators:
      if generator.to_base_length:
        obj = generator.make_object(line, 0)
      else:
        obj = None 
      backgroundobjs.append(obj)
    maxframes = max([ obj.frames for obj in speakervoiceobjs + [ obj for obj in foregroundobjs if obj ] + [ obj for obj in backgroundobjs if obj ]], default=0)
    for index, generator in enumerate(self._foregroundobjectgenerators):
      if not generator.to_base_length:
        foregroundobjs[index] = generator.make_object(line, maxframes)
    for index, generator in enumerate(self._backgroundobjectgenerators):
      if not generator.to_base_length:
        backgroundobjs[index] = generator.make_object(line, maxframes)
    foregroundobjs = [ obj for obj in foregroundobjs if obj ] #remove None in list.
    backgroundobjs = [ obj for obj in backgroundobjs if obj ] #remove None in list.
    for curspeaker in self.curspeakers:
      if self._speakergraphicgenerator:
        obj = self._speakergraphicgenerator.make_object(line, maxframes, curspeaker)
        if obj:
          for postprocessor in self._speakergraphicpostprocessors:
            obj = postprocessor.postprocess(line, obj, curspeaker)
          speakergraphicobjs.append(obj)
      else:
        raise ValueError("{!r}._speakergraphicgenerator is None.".format(self)) #error
    if maxframes:
      for layer, obj in enumerate(speakervoiceobjs, start=1):
        self._speakervoicelayergroup.add_object_to_last(layer, self._offset, obj)
      for layer, obj in enumerate(speakergraphicobjs, start=1):
        self._speakergraphiclayergroup.add_object_to_last(layer, self._offset, obj)
      for layer, obj in enumerate(foregroundobjs, start=1):
        self._foregroundlayergroup.add_object_to_last(layer, self._offset, obj)
      for layer, obj in enumerate(backgroundobjs, start=1):
        self._backgroundlayergroup.add_object_to_last(layer, self._offset, obj)
      self._offset += maxframes

  def feed (self, stream):
    for line in stream:
      self._feed_line(line)

  def _transpile_exo (self):
    exo = EXO(width=self._width, height=self._height, rate=self._framerate, scale=self._scale, audiorate=self._audiorate, audioch=self._audioch)
    layer = 1
    self._backgroundlayergroup.put_to_exo(layer, exo)
    layer += self._backgroundlayergroup.get_total_layer_count()
    self._speakergraphiclayergroup.put_to_exo(layer, exo)
    layer += self._speakergraphiclayergroup.get_total_layer_count()
    self._foregroundlayergroup.put_to_exo(layer, exo)
    layer += self._foregroundlayergroup.get_total_layer_count()
    self._speakervoicelayergroup.put_to_exo(layer, exo)
    layer += self._speakervoicelayergroup.get_total_layer_count()
    exo.fit_length_to_last_object()
    return exo

  def dump (self, stream):
    return self._transpile_exo().dump(stream)

  def dumps (self):
    return self._transpile_exo().dumps()

  @classmethod
  def deserialize (cls, params, *, config, environment):
    transpiler = Transpiler(width=params.get("video", {}).get("width", 1280), height=params.get("video", {}).get("height", 720), framerate=params.get("video", {}).get("frame_rate", 24), scale=params.get("video", {}).get("scale", 1), audiorate=params.get("video", {}).get("audio_rate", 44100), audioch=params.get("video", {}).get("audio_ch", 2), config=config, environment=environment)
    for speakername, speaker in params["speakers"].items():
      spker = Speaker.deserialize(speaker, parent=transpiler, config=config, environment=environment)
      transpiler.add_speaker(speakername, spker)
    voicegenerator = params.get("voice_generator", { "type": "simple" })
    vgen = SpeakerVoiceGenerator.deserialize(voicegenerator, parent=transpiler, config=config, environment=environment)
    transpiler.set_speaker_voice_generator(vgen)
    graphicgenerator = params.get("graphic_generator", { "type": "simple" })
    ggen = SpeakerGraphicGenerator.deserialize(graphicgenerator, parent=transpiler, config=config, environment=environment)
    transpiler.set_speaker_graphic_generator(ggen)
    for postprocessor in params.get("voice_postprocessors", []):
      pp = SpeakerVoicePostProcessor.deserialize(postprocessor, parent=transpiler, config=config, environment=environment)
      transpiler.add_speaker_voice_postprocessor(pp)
    for postprocessor in params.get("graphic_postprocessors", []):
      pp = SpeakerGraphicPostProcessor.deserialize(postprocessor, parent=transpiler, config=config, environment=environment)
      transpiler.add_speaker_graphic_postprocessor(pp)
    for generator in params.get("foreground_object_generators", []):
      gen = ObjectGenerator.deserialize(generator, parent=transpiler, config=config, environment=environment)
      transpiler.add_foreground_object_generator(gen)
    for generator in params.get("background_object_generators", []):
      gen = ObjectGenerator.deserialize(generator, parent=transpiler, config=config, environment=environment)
      transpiler.add_background_object_generator(gen)
    return transpiler
