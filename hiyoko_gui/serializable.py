
import json
from abc import ABC, abstractmethod, abstractclassmethod
from collections.abc import MutableMapping, Mapping

class Serializable (ABC):

  @abstractmethod
  def serialize (self) -> Mapping:
    pass

  @abstractclassmethod
  def deserialize (self, params:MutableMapping, *args, **kwargs) -> "Serializable": 
    pass
