
import re 
from abc import ABC, abstractmethod
from exofile import Color 
from ordered_set import OrderedSet
from .parent_holder import ParentHolder

class Variable (ABC):

  @abstractmethod
  def set (self, value) -> None:
    pass

  @abstractmethod
  def get (self):
    pass

  @abstractmethod
  def clear (self) -> None:
    pass

  @abstractmethod
  def is_assigned (self) -> bool:
    pass

class SingleValueVariable (Variable):

  cast_function = None 

  def __init__ (self):
    self._value = None 

  def set (self, value):
    castedvalue = self.cast_function(value)
    self._value = castedvalue

  def get (self):
    return self._value

  def clear (self):
    self._value = None 

  def is_assigned (self):
    return self._value is not None 

class MultipleValueVariable (Variable):

  cast_function = None 

  def __init__ (self):
    self._values = list()

  def set (self, value):
    castedvalue = self.cast_function(value)
    self._values.append(castedvalue)

  def get (self):
    return self._values.copy()

  def clear (self):
    self._values.clear()

  def is_assigned (self):
    return True 

class MultipleValueSetVariable (Variable):

  cast_function = None 

  def __init__ (self):
    self._values = OrderedSet()

  def set (self, value):
    castedvalue = self.cast_function(value)
    self._values.add(castedvalue)

  def get (self):
    return self._values.copy()

  def clear (self):
    self._values.clear()

  def is_assigned (self):
    return True 

class SpeakersVar (Variable, ParentHolder):
  
  def __init__ (self, *, parent):
    super().__init__(parent=parent)
    self._speakers = OrderedSet()

  def set (self, speakernames):
    spkers = OrderedSet()
    spkernames = re.split(r"[\*&]", speakernames)
    for spkername in spkernames:
      if spkername in self.parent.speakers:
        spkers.add(self.parent.speakers[spkername])
      else:
        raise ValueError("Could not find speaker {!r} in {!r}.".format(spkername, self.parent)) #error
    self._speakers = spkers

  def get (self):
    return self._speakers.copy()

  def clear (self):
    self._speakers.clear()

  def is_assigned (self):
    return True 

class SpeakerVoicesVar (Variable, ParentHolder):
  
  def __init__ (self, *, parent):
    super().__init__(parent=parent)
    self._speakervoices = OrderedSet()

  def set (self, speakervoicenames):
    spkervoices = OrderedSet()
    spkervoicenames = re.split(r"[*&]", speakervoicenames)
    for spkervoicename in spkervoicenames:
      if spkervoicename in self.parent.speakervoices:
        spkervoices.add(self.parent.speakervoices[spkervoicename])
      else:
        raise ValueError("Could not find speakervoice {!r} in {!r}.".format(spkervoicename, self.parent)) #error
    self._speakervoices = spkervoices

  def get (self):
    return self._speakervoices.copy()

  def clear (self):
    self._speakervoices.clear()

  def is_assigned (self):
    return True 

class StringVar (SingleValueVariable):

  cast_function = str 

class IntVar (SingleValueVariable):

  cast_function = int 

class FloatVar (SingleValueVariable):

  cast_function = float 

class BooleanVar (SingleValueVariable):

  @staticmethod
  def cast_function (val): #convert val to str -> int -> bool.
    return bool(int(val))

class ColorVar (SingleValueVariable):

  cast_function = Color.deserialize

class StringsVar (MultipleValueVariable):

  cast_function = str 

class IntsVar (MultipleValueVariable):

  cast_function = int 

class FloatsVar (MultipleValueVariable):

  cast_function = float 

class BooleansVar (MultipleValueVariable):

  @staticmethod
  def cast_function (val): #convert val to str -> int -> bool.
    return bool(int(val))

class ColorsVar (MultipleValueVariable):

  cast_function = Color.deserialize

class StringSetVar (MultipleValueSetVariable):

  cast_function = str 

class IntSetVar (MultipleValueSetVariable):

  cast_function = int 

class FloatSetVar (MultipleValueSetVariable):

  cast_function = float 

class BooleanSetVar (MultipleValueSetVariable):

  @staticmethod
  def cast_function (val): #convert val to str -> int -> bool.
    return bool(int(val))

class ColorSetVar (MultipleValueSetVariable):

  cast_function = Color.deserialize
