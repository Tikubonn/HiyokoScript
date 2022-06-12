
from abc import ABC
from collections.abc import Mapping

class LanguageHolder (ABC):

  def __init__ (self, *, language:Mapping):
    self._language = dict(language)

  @property
  def language (self) -> Mapping:
    return self._language 

  def translate (self, id, *args, **kwargs) -> str:
    return self._language[id].format(*args, **kwargs)
