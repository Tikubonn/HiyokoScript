
from .psdtoolkit_object_0_1_3 import PSDToolKitLipSyncPreparationObject_0_1_3
from .speaker_voice_postprocessor import SpeakerVoicePostProcessor

class PSDToolKitLipSyncPreparationPostProcessor_0_1_3 (SpeakerVoicePostProcessor):

  def __init__ (self, *, parent, config, lowcut=100, highcut=1000, threshold=0.333):
    super().__init__(parent=parent, config=config)
    self.lowcut = lowcut
    self.highcut = highcut
    self.threshold = threshold

  def postprocess (self, text, obj, speakervoice):
    return PSDToolKitLipSyncPreparationObject_0_1_3(
      obj, 
      parent=self.parent, 
      config=self.config,
      lowcut=self.lowcut,
      highcut=self.highcut,
      threshold=self.threshold,
    )

  @classmethod
  def deserialize (cls, params, *, parent, config):
    return cls(
      parent=parent,
      config=config,
      lowcut=params.get("low_cut", 100),
      highcut=params.get("high_cut", 1000),
      threshold=params.get("threshold", 0.333),
    )
