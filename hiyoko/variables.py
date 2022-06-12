
class Variables:

  def __init__ (self):
    self.variables = dict()

  def register (self, name, variable):
    self.variables[name] = variable

  def set (self, name, value):
    if name in self.variables:
      return self.variables[name].set(value)
    else:
      raise KeyError("Could not find variable {!r} in {!r}.".format(name, self)) #error

  def get (self, name):
    if name in self.variables:
      return self.variables[name].get()
    else:
      raise KeyError("Could not find variable {!r} in {!r}.".format(name, self)) #error
  
  def clear (self, name):
    if name in self.variables:
      return self.variables[name].clear()
    else:
      raise KeyError("Could not find variable {!r} in {!r}.".format(name, self)) #error
