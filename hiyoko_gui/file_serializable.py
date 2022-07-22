
import json 
import tkinter as tk 
import tkinter.ttk 
from abc import abstractclassmethod
from hiyoko import SwappedFile
from pathlib import Path 
from .serializable import Serializable

class FileSerializable (Serializable):

  def serialize_to_file (self, file) -> None:
    with SwappedFile(file, "w", encoding="utf-8") as stream:
      params = self.serialize()
      json.dump(params, stream, ensure_ascii=False, indent=2)

  @abstractclassmethod
  def deserialize (cls, params, file=None, *args, **kwargs) -> "FileSerializable":
    pass

  @classmethod
  def deserialize_from_file (cls, file, *args, **kwargs) -> "FileSerializable":
    with open(file, "r", encoding="utf-8") as stream:
      params = json.load(stream)
      return cls.deserialize(params, file, *args, **kwargs)
