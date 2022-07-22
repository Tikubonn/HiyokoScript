
import json5
import tkinter as tk 
import tkinter.messagebox
import traceback
from pathlib import Path 
from argparse import ArgumentParser 
from hiyoko_gui import EditorWindow

def main ():
  parser = ArgumentParser()
  parser.add_argument("--config-file", type=Path, default="./config.json")
  parser.add_argument("--language-file", type=Path, default="./language.editor.json")
  parser.add_argument("--history-file", type=Path, default="./history.editor.json")
  args = parser.parse_args()
  with open(args.config_file, "r", encoding="utf-8") as stream:
    config = json5.load(stream)
  with open(args.language_file, "r", encoding="utf-8") as stream:
    language = json5.load(stream)
  if Path(args.history_file).exists():
    try:
      window = EditorWindow.deserialize_from_file(args.history_file, config=config, language=language)
    except:
      tk.messagebox.showwarning(
        language["error_load_history_file"],
        language["error_load_history_file_desc"]
      )
      traceback.print_exc()
      window = EditorWindow(config=config, language=language, configfile=Path("./config.json"), historyfile=args.history_file)
  else:
    window = EditorWindow(config=config, language=language, configfile=Path("./config.json"), historyfile=args.history_file)
  window.iconbitmap(default="./picture/HiyokoScriptEditor.ico")
  window.mainloop()

if __name__ == "__main__":
  main()
