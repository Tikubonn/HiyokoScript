
import re
from abc import ABC, abstractmethod

class SyntaxProcessor (ABC):

  def __init__ (self, parent):
    self.parent = parent

  @abstractmethod
  def process (self, line) -> (bool, str):
    pass

class CommentOut (SyntaxProcessor):

  def process (self, line):
    if line.startswith("--"):
      return True, ""
    else:
      return False, ""

class SetSpeakerVoice (SyntaxProcessor): 

  def _find_name_and_speaker_voice_by_line (self, line):
    names = sorted(self.parent.speakervoices.keys(), key=len, reverse=True)
    for name in names:
      if line.startswith(name):
        return name, self.parent.speakervoices[name]
    else:
      raise ValueError("Could not find voice name by {!r} in {!r}.".format(line, self.parent)) #error 

  def process (self, line):
    if line.startswith("#"):
      line = line[1:]
      speakervoices = list()
      while line:
        if speakervoices:
          if line.startswith("&") or line.startswith("*"):
            line = line[1:]
          else:
            break
        name, speakervoice = self._find_name_and_speaker_voice_by_line(line)
        speakervoices.append(speakervoice)
        line = line[len(name):]
      self.parent.curspeakervoices.clear()
      self.parent.curspeakervoices.update(speakervoices)
      return True, line
    else:
      return False, ""

class SetSpeaker (SyntaxProcessor):

  def _find_name_and_speaker_by_line (self, line):
    names = sorted(self.parent.speakers.keys(), key=len, reverse=True)
    for name in names:
      if line.startswith(name):
        return name, self.parent.speakers[name]
    else:
      raise ValueError("Could not find speaker name by {!r} in {!r}.".format(line, self.parent)) #error 

  def process (self, line):
    if line.startswith("@"):
      line = line[1:]
      speakers = list()
      while line:
        if speakers:
          if line.startswith("&") or line.startswith("*"):
            line = line[1:]
          else:
            break
        name, speaker = self._find_name_and_speaker_by_line(line)
        speakers.append(speaker)
        line = line[len(name):]
      self.parent.curspeakers.clear()
      self.parent.curspeakers.update(speakers)
      return True, line
    else:
      return False, ""

class SetVariable (SyntaxProcessor):

  def process (self, line):
    if line.startswith("$"):
      line = line[1:]
      matchresult = re.match(r"(.+?)=(.*)$", line)
      if matchresult:
        name, value = matchresult.groups()
        self.parent.variables.set(name, value)
        return True, ""
      matchresult = re.match(r"(.+?)$", line)
      if matchresult:
        name, = matchresult.groups()
        self.parent.variables.clear(name)
        return True, ""
      raise ValueError("Require some characters after $.") #error 
    else:
      return False, ""
