
import sys 
import json5
from hiyoko import Transpiler, SwappedFile, open_stdin, open_stdout, resolve_config
from pathlib import Path
from argparse import ArgumentParser

def _open_input_file (file):
  if file is not None:
    return open(file, "r", encoding="utf-8")
  else:
    return open_stdin("r")

def _open_output_file (file):
  if file is not None:
    return SwappedFile(file, "w", encoding="cp932") #encoding must be cp932!
  else:
    return open_stdout("w")

def transpile (*, inputfile, configfile, outputfile):
  try:
    with open(configfile, "r", encoding="utf-8") as stream:
      config = json5.load(stream)
      config = resolve_config(config)
    environment = dict()
    if inputfile is not None:
      environment["search_paths"] = [ Path(inputfile).parent.absolute() ]
    transpiler = Transpiler.deserialize(config, config=config, environment=environment)
    with _open_input_file(inputfile) as stream:
      transpiler.feed(stream)
    with _open_output_file(outputfile) as stream:
      transpiler.dump(stream)
  except KeyboardInterrupt:
    print("Received keyboard interrupt.", file=sys.stderr) #abort application.

def main ():
  parser = ArgumentParser()
  parser.add_argument("file", help="An input file, if exec this without this parameter, this use the stdin.", nargs="?", type=Path, default=None)  
  parser.add_argument("--config-file", help="A JSON formatted configuration file, if exec this without this parameter, this try open ./config.json.", type=Path, default="./config.json")
  parser.add_argument("--output-file", "-o", help="An output file, if exec this without this parameter, this use the stdout.", type=Path, default=None)
  args = parser.parse_args()
  transpile(
    inputfile=args.file,
    configfile=args.config_file,
    outputfile=args.output_file,
  )

if __name__ == "__main__":
  main()
