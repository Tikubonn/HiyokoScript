
import os
from pathlib import Path 

def search_file (file, *, config, environment):
  f = Path(file)
  if f.exists():
    return f
  else:
    searchpaths = config.get("search_paths", []) + environment.get("search_paths", []) + [ "." ]
    for searchpath in searchpaths:
      foundfiles = list(Path(searchpath).rglob(str(f)))
      if foundfiles:
        return foundfiles[0]
    else:
      raise ValueError("Could not find file {!r} in {!r}.".format(f, searchpaths)) #error

def create_file (path, mode, *args, createdirectories=True, directoriesexistok=True, **kwargs):
  p = Path(path)  
  if createdirectories:
    os.makedirs(p.parent, exist_ok=directoriesexistok)
  return open(path, mode, *args, **kwargs)

RESERVED_CHARACTERS = "<>:\"/\\|?*"

def safe_stem (stem):
  s = stem
  for char in RESERVED_CHARACTERS:
    s = s.replace(char, "")
  return s 

def safe_path (path):
  p = Path(path)
  p = p.with_stem(safe_stem(p.stem))
  return p 
