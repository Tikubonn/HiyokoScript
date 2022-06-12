
from exolib import PositionRange, InsertionMode

class LayerGroup:

  def __init__ (self):
    self._layerobjects = [ list() for layer in range(1, 99 +1) ]

  def add_object_to_last (self, layer, offset, obj):
    if self._layerobjects[layer -1]:
      lastoffset, lastobj = self._layerobjects[layer -1][-1]
      lastend = lastoffset + lastobj.frames 
      if lastend == offset:
        if lastobj.is_mergeable(obj):
          self._layerobjects[layer -1][-1] = (lastoffset, lastobj.merge(obj))
        else:
          self._layerobjects[layer -1].append((offset, obj))
      else:
        self._layerobjects[layer -1].append((offset, obj))
    else:
      self._layerobjects[layer -1].append((offset, obj))

  def get_total_layer_count_at (self, layer):
    return max((len(obj.try_make_objnodes()) for offset, obj in self._layerobjects[layer -1]), default=0)

  def get_total_layer_count (self):
    return sum((self.get_total_layer_count_at(layer) for layer in range(1, 99 +1)))

  def put_to_exo (self, layer, exo):
    ly = layer
    for ily, objs in enumerate(self._layerobjects, start=1):
      for offset, obj in objs:
        for il, objnode in enumerate(obj.try_make_objnodes()):
          exo.insert_object(ly + il, PositionRange(offset, offset + obj.frames -1), objnode, InsertionMode.NONE)
      ly += self.get_total_layer_count_at(ily)
