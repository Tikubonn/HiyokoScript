
import sys 
import json5
import traceback
import subprocess
from hiyoko import Transpiler, build_config
from pathlib import Path
from tkinter import messagebox
from datetime import datetime
from argparse import ArgumentParser

def _open_input_file (file):
  if file is not None:
    return open(file, "r", encoding="utf-8")
  else:
    return sys.stdin

def _open_output_file (file):
  if file is not None:
    return open(file, "w", encoding="cp932") #encoding must be cp932!
  else:
    return sys.stdout

def _make_error_log_file ():
  now = datetime.now()
  return "error-log-{:s}.txt".format(now.strftime("%Y%m%d-%H%M%S")) #like as error-log-20220312-001230.txt

def transpile (*, inputfile, configfile, outputfile, languagefile, notifymessage=False):
  try:
    with open(configfile, "r", encoding="utf-8") as stream:
      config = json5.load(stream)
      config = build_config(config)
    environment = dict()
    if inputfile is not None:
      environment["search_paths"] = [ Path(inputfile).parent.absolute() ]
    with open(languagefile, "r", encoding="utf-8") as stream:
      language = json5.load(stream)
    transpiler = Transpiler.deserialize(config, config=config, environment=environment)
    if notifymessage:
      messagebox.showinfo(
        language["transpile_start"],
        language["transpile_start_desc"]
      )
    with _open_input_file(inputfile) as stream:
      transpiler.feed(stream)
    with _open_output_file(outputfile) as stream:
      transpiler.dump(stream)
    if notifymessage:
      messagebox.showinfo(
        language["transpile_end"],
        language["transpile_end_desc"]
      )
  except:
    if notifymessage:
      messagebox.showerror(
        language["transpile_errored"],
        language["transpile_errored_desc"]
      )
      errorlogfile = _make_error_log_file()
      with open(errorlogfile, "w", encoding="utf-8") as stream:
        traceback.print_exc(file=stream)
      subprocess.run([ "start", "explorer", errorlogfile ], shell=True, check=True)
    raise

def main ():
  parser = ArgumentParser()
  parser.add_argument("file", help="An input file, if exec this without this parameter, this use the stdin.", nargs="?", type=Path, default=None)  
  parser.add_argument("--config-file", help="A JSON formatted configuration file, if exec this without this parameter, this try open ./config.json.", type=Path, default="./config.json")
  parser.add_argument("--output-file", "-o", help="An output file, if exec this without this parameter, this use the stdout.", type=Path, default=None)
  parser.add_argument("--language-file", help="A JSON formatted configuration file, if exec this without this parameter, this try open ./language.json.", type=Path, default="./language.json")
  parser.add_argument("--notify-message", help="Notify messages with GUI window. This is internal option for HiyokoScriptGUI.", action="store_true")
  args = parser.parse_args()
  transpile(
    inputfile=args.file,
    configfile=args.config_file,
    outputfile=args.output_file,
    languagefile=args.language_file,
    notifymessage=args.notify_message
  )

if __name__ == "__main__":
  main()
