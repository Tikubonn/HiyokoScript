
import json5
from collections.abc import Mapping, Iterable 

def resolve_config (config): #imports指定された設定ファイルをすべて統合した辞書を返します。
  conf = config.copy()
  confimps = conf.pop("imports", [])
  if isinstance(confimps, Iterable):
    while confimps:
      confimp = confimps.pop(0)
      with open(confimp, "r", encoding="utf-8") as stream:
        impconf = json5.load(stream)
      for key, value in impconf.items():
        if key == "imports":
          if isinstance(value, Iterable):
            confimps = list(value) + confimps 
          else:
            raise TypeError("Parameter .imports {!r} must be iterable.".format(value)) #error 
        else:
          if isinstance(value, Mapping):
            if key in conf:
              if isinstance(conf[key], Mapping):
                conf[key].update(value)
              else:
                raise TypeError("Parameter .{:s} {!r} and {!r} are type mismatched.".format(key, value, conf[key])) #error 
            else:
              conf[key] = value
          elif isinstance(value, Iterable):
            if key in conf:
              if isinstance(conf[key], Iterable):
                conf[key].extend(value)
              else:
                raise TypeError("Parameter .{:s} {!r} and {!r} are type mismatched.".format(key, value, conf[key])) #error 
            else:
              conf[key] = value
          else:
            conf[key] = value
  else:
    raise TypeError("Parameter .imports {!r} must be iterable.".format(confimps)) #error 
  return conf 
