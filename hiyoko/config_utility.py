
import json5
from collections.abc import Mapping, Iterable 

def build_config (config): #imports指定された設定ファイルをすべて統合した辞書を返します。
  conf = config.copy()
  while conf.get("imports", []):
    imports = conf.get("imports", [])
    conf["imports"] = []
    for imp in imports:
      with open(imp, "r", encoding="utf-8") as stream:
        impconf = json5.load(stream)
      for key, value in impconf.items():
        if key in conf:
          if isinstance(conf[key], Mapping):
            if isinstance(value, Mapping):
              conf[key].update(value)
            else:
              raise TypeError()
          elif isinstance(conf[key], Iterable):
            if isinstance(value, Iterable):
              conf[key].extend(value)
            else:
              raise TypeError()
          else:
            conf[key] = value
        else:
          conf[key] = value
  return conf 
