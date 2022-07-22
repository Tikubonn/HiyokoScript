
import os 
import json5
from hiyoko import resolve_config 
from tempfile import NamedTemporaryFile
from unittest import TestCase 

class TestResolveConfig (TestCase):

  def test_resolve_config (self):
    examplefile1 = NamedTemporaryFile(mode="w", delete=False)
    examplefile2 = NamedTemporaryFile(mode="w", delete=False)
    examplefile3 = NamedTemporaryFile(mode="w", delete=False)
    json5.dump({ "example": [ 1 ], "imports": [ examplefile2.name ] }, examplefile1)
    json5.dump({ "example": [ 2 ], "imports": [ examplefile3.name ] }, examplefile2)
    json5.dump({ "example": [ 3 ], "imports": [] }, examplefile3)
    examplefile1.close()
    examplefile2.close()
    examplefile3.close()
    config = { "imports": [ examplefile1.name ] }    
    resolvedconfig = resolve_config(config)

    self.assertEqual("imports" in resolvedconfig, False)
    self.assertEqual("example" in resolvedconfig, True)
    self.assertEqual(resolvedconfig["example"], [ 1, 2, 3 ])

    os.remove(examplefile1.name)
    os.remove(examplefile2.name)
    os.remove(examplefile3.name)

  def test_resolve_config2 (self):
    examplefile1 = NamedTemporaryFile(mode="w", delete=False)
    examplefile2 = NamedTemporaryFile(mode="w", delete=False)
    examplefile3 = NamedTemporaryFile(mode="w", delete=False)
    json5.dump({ "example": { "one": 1 }, "imports": [ examplefile2.name ] }, examplefile1)
    json5.dump({ "example": { "two": 2 }, "imports": [ examplefile3.name ] }, examplefile2)
    json5.dump({ "example": { "three": 3 }, "imports": [] }, examplefile3)
    examplefile1.close()
    examplefile2.close()
    examplefile3.close()
    config = { "imports": [ examplefile1.name ] }    
    resolvedconfig = resolve_config(config)

    self.assertEqual("imports" in resolvedconfig, False)
    self.assertEqual("example" in resolvedconfig, True)
    self.assertEqual(resolvedconfig["example"], { "one": 1, "two": 2, "three": 3 })

    os.remove(examplefile1.name)
    os.remove(examplefile2.name)
    os.remove(examplefile3.name)

  def test_resolve_config3 (self):
    examplefile1 = NamedTemporaryFile(mode="w", delete=False)
    examplefile2 = NamedTemporaryFile(mode="w", delete=False)
    examplefile3 = NamedTemporaryFile(mode="w", delete=False)
    json5.dump({ "example": 1, "imports": [ examplefile2.name ] }, examplefile1)
    json5.dump({ "example": 2, "imports": [ examplefile3.name ] }, examplefile2)
    json5.dump({ "example": 3, "imports": [] }, examplefile3)
    examplefile1.close()
    examplefile2.close()
    examplefile3.close()
    config = { "imports": [ examplefile1.name ] }    
    resolvedconfig = resolve_config(config)

    self.assertEqual("imports" in resolvedconfig, False)
    self.assertEqual("example" in resolvedconfig, True)
    self.assertEqual(resolvedconfig["example"], 3)

    os.remove(examplefile1.name)
    os.remove(examplefile2.name)
    os.remove(examplefile3.name)
