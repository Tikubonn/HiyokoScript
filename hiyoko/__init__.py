
from .layer_group import LayerGroup
from .parent_holder import ParentHolder 
from .config import resolve_config
from .config_holder import ConfigHolder 
from .deserializable import Deserializable
from .object import Object, GeneratedObject, CharacterGraphicObject, SEObject, BGMObject, ColorBackgroundObject, ImageBackgroundObject, VideoBackgroundObject, CinemaScopeObject, SubtitleObject, FilterObject, BounceObject, RasterObject, HoppingObject 
from .object_generator import ObjectGenerator, ColorBackgroundGenerator, ImageBackgroundGenerator, VideoBackgroundGenerator, CinemaScopeGenerator, SubtitleGenerator, SEGenerator, BGMGenerator
from .file_utility import create_file, search_file, safe_path
from .speaker import Speaker
from .speaker_graphic import SpeakerGraphic, CopySpeakerGraphic, SimpleSpeakerGraphic
from .speaker_graphic_generator import SpeakerGraphicGenerator, SimpleSpeakerGraphicGenerator 
from .speaker_graphic_postprocessor import SpeakerGraphicPostProcessor, BouncePostProcessor, BounceAtSpeakingPostProcessor, RasterPostProcessor, HoppingPostProcessor, HoppingAtSpeakingPostProcessor
from .speaker_voice import SpeakerVoice, CopySpeakerVoice, VoiceVoxSpeakerVoiceStyle, VoiceVoxSpeakerVoice, SoftalkSpeakerVoiceNameType, SoftalkSpeakerVoiceName, SoftalkSpeakerVoice, AssistantSeikaSpeakerVoice
from .speaker_voice_generator import SpeakerVoiceGenerator, SimpleSpeakerVoiceGenerator 
from .speaker_voice_postprocessor import SpeakerVoicePostProcessor
from .syntax_processor import SyntaxProcessor, CommentOut, SetSpeakerVoice, SetSpeaker, SetVariable
from .transpiler import Transpiler 
from .variable import Variable, SingleValueVariable, MultipleValueVariable, MultipleValueSetVariable, SpeakersVar, SpeakerVoicesVar, StringVar, IntVar, FloatVar, BooleanVar, ColorVar, StringsVar, IntsVar, FloatsVar, BooleansVar, ColorsVar, StringSetVar, IntSetVar, FloatSetVar, BooleanSetVar, ColorSetVar
from .variables import Variables
from .psdtoolkit_object_0_1_3 import PSDToolKitLipSyncPreparationObject_0_1_3, PSDToolKitObject_0_1_3
from .psdtoolkit_speaker_graphic_0_1_3 import PSDToolKitSpeakerGraphic_0_1_3
from .psdtoolkit_speaker_voice_postprocessor_0_1_3 import PSDToolKitLipSyncPreparationPostProcessor_0_1_3
from .psdtoolkit_object_0_2 import PSDToolKitLipSyncPreparationObject_0_2, PSDToolKitObject_0_2
from .psdtoolkit_speaker_graphic_0_2 import PSDToolKitSpeakerGraphic_0_2
from .psdtoolkit_speaker_voice_postprocessor_0_2 import PSDToolKitLipSyncPreparationPostProcessor_0_2
from .temp_symlink import TempSymLink
from .environment_holder import EnvironmentHolder
from .swapped_file import SwappedFile 
from .file import open_stdin, open_stdout, open_stderr

SpeakerVoice.speaker_voice_type_table = SpeakerVoice.speaker_voice_type_table | {
  "copy": CopySpeakerVoice, 
  "voicevox": VoiceVoxSpeakerVoice,
  "softalk": SoftalkSpeakerVoice,
  "assistant_seika": AssistantSeikaSpeakerVoice,
}

SpeakerGraphic.speaker_graphic_type_table = SpeakerGraphic.speaker_graphic_type_table | {
  "copy": CopySpeakerGraphic,
  "simple": SimpleSpeakerGraphic,
  "psdtoolkit_0.1.3": PSDToolKitSpeakerGraphic_0_1_3,
  "psdtoolkit_0.2": PSDToolKitSpeakerGraphic_0_2,
}

SpeakerVoiceGenerator.speaker_voice_generator_type_table = SpeakerVoiceGenerator.speaker_voice_generator_type_table | {
  "simple": SimpleSpeakerVoiceGenerator,
}

SpeakerGraphicGenerator.speaker_graphic_generator_type_table = SpeakerGraphicGenerator.speaker_graphic_generator_type_table | {
  "simple": SimpleSpeakerGraphicGenerator,
}

SpeakerVoicePostProcessor.speaker_voice_postprocessor_type_table = SpeakerVoicePostProcessor.speaker_voice_postprocessor_type_table | {
  "psdtoolkit_0.1.3_lipsync_preparation": PSDToolKitLipSyncPreparationPostProcessor_0_1_3,
  "psdtoolkit_0.2_lipsync_preparation": PSDToolKitLipSyncPreparationPostProcessor_0_2,
}

SpeakerGraphicPostProcessor.speaker_graphic_postprocessor_type_table = SpeakerGraphicPostProcessor.speaker_graphic_postprocessor_type_table | {
  "bounce": BouncePostProcessor,
  "bounce_at_speaking": BounceAtSpeakingPostProcessor,
  "hopping": HoppingPostProcessor,
  "hopping_at_speaking": HoppingAtSpeakingPostProcessor,
  "raster": RasterPostProcessor,
}

ObjectGenerator.object_generator_type_table = ObjectGenerator.object_generator_type_table | {
  "color_background": ColorBackgroundGenerator,  
  "image_background": ImageBackgroundGenerator,  
  "video_background": VideoBackgroundGenerator,  
  "cinema_scope": CinemaScopeGenerator,  
  "subtitle": SubtitleGenerator,  
  "se": SEGenerator,  
  "bgm": BGMGenerator, 
}

Transpiler.syntax_processor_types = Transpiler.syntax_processor_types + [
  CommentOut, 
  SetSpeakerVoice, 
  SetSpeaker, 
  SetVariable,
]
