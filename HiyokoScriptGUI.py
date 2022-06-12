
import json5
from pathlib import Path 
from tkinter import messagebox
from argparse import ArgumentParser 
from hiyoko_gui import MainWindow

def main ():
  parser = ArgumentParser()
  parser.add_argument("--config-file", type=Path, default="./config.json")
  parser.add_argument("--language-file", type=Path, default="./language.gui.json")
  parser.add_argument("--history-file", type=Path, default="./history.gui.json")
  args = parser.parse_args()
  with open(args.config_file, "r", encoding="utf-8") as stream:
    config = json5.load(stream)
  with open(args.language_file, "r", encoding="utf-8") as stream:
    language = json5.load(stream)
  if Path(args.history_file).exists():
    try:
      window = MainWindow.deserialize_from_file(args.history_file, config=config, language=language)
    except:
      messagebox.showwarning(
        language["error_load_history_file"],
        language["error_load_history_file_desc"]
      )
      window = MainWindow(config=config, language=language, defaultconfigfile=Path("./config.json"), serializefile=args.history_file)
  else:
    window = MainWindow(config=config, language=language, defaultconfigfile=Path("./config.json"), serializefile=args.history_file)
  window.iconbitmap(default="./icon/HiyokoScriptGUI.ico")
  window.mainloop()

if __name__ == "__main__":
  main()
