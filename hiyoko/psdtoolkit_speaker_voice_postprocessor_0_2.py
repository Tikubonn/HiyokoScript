
from .psdtoolkit_object_0_2 import PSDToolKitLipSyncPreparationObject_0_2
from .speaker_voice_postprocessor import SpeakerVoicePostProcessor

class PSDToolKitLipSyncPreparationPostProcessor_0_2 (SpeakerVoicePostProcessor):

  def __init__ (self, *, parent, config, environment, lowcut=100, highcut=1000, threshold=20, sensitivity=1):
    super().__init__(parent=parent, config=config, environment=environment)
    self.lowcut = lowcut
    self.highcut = highcut
    self.threshold = threshold
    self.sensitivity = sensitivity

  def postprocess (self, text, obj, speakervoice):
    return PSDToolKitLipSyncPreparationObject_0_2(
      obj, 
      parent=self.parent, 
      config=self.config,
      environment=self.environment,
      lowcut=self.lowcut,
      highcut=self.highcut,
      threshold=self.threshold,
      sensitivity=self.sensitivity,
    )

  @classmethod
  def deserialize (cls, params, *, parent, config, environment):
    return cls(
      parent=parent,
      config=config,
      environment=environment,
      lowcut=params.get("low_cut", 100),
      highcut=params.get("high_cut", 1000),
      threshold=params.get("threshold", 20),
      sensitivity=params.get("sensitivity", 1),
    )
