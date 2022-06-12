
from abc import ABC, abstractclassmethod

class Deserializable (ABC):

  @abstractclassmethod
  def deserialize (cls, params, *args, **kwargs) -> "Deserializable":
    pass
