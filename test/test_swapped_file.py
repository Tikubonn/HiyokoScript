
import os 
import tempfile 
from hiyoko import SwappedFile
from pathlib import Path 
from unittest import TestCase 

class TestSwappedFile (TestCase):

  def test_swapped_file (self):
    destpath = tempfile.mktemp()
    file = SwappedFile(destpath, "w", encoding="utf-8")
    file.write("example")
    file.close()
    file.swap()
    self.assertEqual(Path(file.name).exists(), False)
    self.assertEqual(Path(destpath).exists(), True)
    with open(destpath, "r", encoding="utf-8") as stream:
      self.assertEqual(stream.read(), "example")
    os.remove(destpath) 

  def test_swapped_file2 (self):
    destpath = tempfile.mktemp()
    with SwappedFile(destpath, "w", encoding="utf-8") as file:
      file.write("example")
    self.assertEqual(Path(file.name).exists(), False)
    self.assertEqual(Path(destpath).exists(), True)
    with open(destpath, "r", encoding="utf-8") as stream:
      self.assertEqual(stream.read(), "example")
    os.remove(destpath) 

  def test_swapped_file3 (self):
    destpath = tempfile.mktemp()
    file = SwappedFile(destpath, "w+b")
    file.write(b"example")
    file.close()
    file.swap()
    self.assertEqual(Path(file.name).exists(), False)
    self.assertEqual(Path(destpath).exists(), True)
    with open(destpath, "rb") as stream:
      self.assertEqual(stream.read(), b"example")
    os.remove(destpath) 

  def test_swapped_file4 (self):
    destpath = tempfile.mktemp()
    with SwappedFile(destpath, "w+b") as file:
      file.write(b"example")
    self.assertEqual(Path(file.name).exists(), False)
    self.assertEqual(Path(destpath).exists(), True)
    with open(destpath, "rb") as stream:
      self.assertEqual(stream.read(), b"example")
    os.remove(destpath) 

  def test_swapped_file5 (self):
    destpath = tempfile.mktemp()
    try:
      with SwappedFile(destpath, "w", encoding="utf-8") as file:
        file.write("example")
        raise Exception()
    except:
      pass
    self.assertEqual(Path(file.name).exists(), False)
    self.assertEqual(Path(destpath).exists(), False)

  def test_swapped_file6 (self):
    destpath = tempfile.mktemp()
    try:
      with SwappedFile(destpath, "wb") as file:
        file.write(b"example")
        raise Exception()
    except:
      pass
    self.assertEqual(Path(file.name).exists(), False)
    self.assertEqual(Path(destpath).exists(), False)
