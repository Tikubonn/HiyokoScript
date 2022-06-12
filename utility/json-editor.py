
import re 
import json 
import json5
from pathlib import Path 
from argparse import ArgumentParser, REMAINDER
from enum import Enum, auto, unique

"""
python json-editor.py example.json --set a.b.c 10 => { "a": { "b": { "c": 10 }}}
python json-editor.py example.json --delete a.b.c1 => { "a": { "b": { "c2": 2, "c3": 3 }}}
"""

class EditMode (Enum):

  NONE = 0
  SET = auto()
  DELETE = auto()

def set_config (query, config):
  match = re.match(r"^(.+?)=(.+?)$", query)
  if match:
    path, value = match.groups()
    conf = config 
    keys = path.split(".")
    for key in keys[:-1]:
      conf = conf.get(key, {})
    conf[keys[-1]] = json5.loads(value)
  else:
    raise ValueError()

def delete_config (query, config):
  conf = config
  keys = query.split(".")
  for key in keys[:-1]:
    conf = conf.get(key, {})
  if keys[-1] in conf:
    del conf[keys[-1]]

def main ():
  parser = ArgumentParser()
  parser.add_argument("file", type=Path)
  parser.add_argument("queries", nargs=REMAINDER)
  args = parser.parse_args()
  with open(args.file, "r", encoding="utf-8") as stream:
    config = json5.load(stream)
  editmode = EditMode.NONE
  for query in args.queries:
    if query == "--set":
      editmode = EditMode.SET
    elif query == "--delete":
      editmode = EditMode.DELETE
    elif editmode == EditMode.SET:
      set_config(query, config)
    elif editmode == EditMode.DELETE:
      delete_config(query, config)
    else:
      raise ValueError()

  with open(args.file, "w", encoding="utf-8") as stream:
    json.dump(config, stream, ensure_ascii=False, indent=2)

if __name__ == "__main__":
  main()
