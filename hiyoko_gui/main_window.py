
import json 
import tkinter 
import subprocess
from pathlib import Path 
from .file_selector import FileSelector
from .file_selector_widget import FileSelectorWidget
from .language_holder import LanguageHolder
from .serializable import Serializable
from .constants import PADDING, WINDOW_PADDING, WORDWRAP_WIDTH, FONT, FONT_BOLD
from .config_holder import ConfigHolder 

"""
+----------------------------------------+
| title                        [_][O][x] |
+----------------------------------------+
| description                            |
|                                        |
+----------------------------------------+
| input-file  [ file ][ select ][ open ] |
| config-file [ file ][ select ][ open ] |
+----------------------------------------+
| [ help ]          [ close ][ execute ] |
+----------------------------------------+
"""

class MainWindow (tkinter.Tk, Serializable, ConfigHolder, LanguageHolder):
  
  def __init__ (self, *, config, language, defaultinputfile=None, defaultconfigfile=None, defaultoutputfile=None, serializefile=None):
    tkinter.Tk.__init__(self)
    ConfigHolder.__init__(self, config=config)
    LanguageHolder.__init__(self, language=language)
    self.inputfile = None 
    self.configfile = None 
    self.outputfile = FileSelector(defaultoutputfile, filetypes=[ (self.translate("output_file_type"), "*.exo") ], assave=True)
    self.serializefile = serializefile
    self._setup_widgets(defaultinputfile=defaultinputfile, defaultconfigfile=defaultconfigfile)

  def _execute (self):
    if not self.inputfile.selectedfile:
      tkinter.messagebox.showwarning(
        self.translate("warning_input_file_is_unspecified"),
        self.translate("warning_input_file_is_unspecified_desc")
      )
      return #abort!
    if not self.configfile.selectedfile:
      tkinter.messagebox.showwarning(
        self.translate("warning_config_file_is_unspecified"),
        self.translate("warning_config_file_is_unspecified_desc")
      )
      return #abort!
    if not self.outputfile.select_file():
      return #abort if canceled.
    if not self.outputfile.selectedfile:
      tkinter.messagebox.showwarning(
        self.translate("warning_output_file_is_unspecified"),
        self.translate("warning_output_file_is_unspecified_desc")
      )
      return #abort!
    command = [ "start" ] + self.hiyokoconfig.get("hiyoko_script", {}).get("hiyoko_script_command", "HiyokoScript.exe").split(" ") + [ str(self.inputfile.selectedfile.absolute()), "--config-file", str(self.configfile.selectedfile.absolute()), "--output-file", str(self.outputfile.selectedfile.absolute()), "--notify-message" ]
    subprocess.run(command, shell=True)

  def destroy (self):
    try:
      if self.serializefile:
        self.serialize_to_file(self.serializefile)
    finally:
      super().destroy()

  def _help (self):
    subprocess.run([ "start", "explorer", str(Path("./README.md").absolute()) ], shell=True, check=True)

  def _setup_widgets (self, *, defaultinputfile=None, defaultconfigfile=None): #tmp
    self.title(self.translate("title"))
    frame = tkinter.Frame(self)
    frame.pack(padx=WINDOW_PADDING, pady=WINDOW_PADDING)
    descframe = tkinter.Frame(frame)
    descframe.pack(padx=PADDING, pady=PADDING)
    desclabel = tkinter.Label(descframe, text=self.translate("description"), wraplength=WORDWRAP_WIDTH, justify=tkinter.LEFT, font=FONT)
    desclabel.pack()

    fileframe = tkinter.Frame(frame)
    fileframe.pack(padx=PADDING, pady=PADDING)
    inputfilelabel = tkinter.Label(fileframe, text=self.translate("label_input_file"), font=FONT)
    inputfilelabel.grid(row=0, column=0, padx=PADDING, pady=PADDING, sticky=tkinter.W)
    inputfile = FileSelectorWidget(defaultinputfile, fileframe, language=self.language, filetypes=[ (self.translate("input_file_type"), "*.txt") ], assave=False)
    inputfile.grid(row=0, column=1, padx=PADDING, pady=PADDING, in_=fileframe)
    self.inputfile = inputfile
    configfilelabel = tkinter.Label(fileframe, text=self.translate("label_config_file"), font=FONT)
    configfilelabel.grid(row=1, column=0, padx=PADDING, pady=PADDING, sticky=tkinter.W)
    configfile = FileSelectorWidget(defaultconfigfile, fileframe, language=self.language, filetypes=[ (self.translate("config_file_type"), "*.json") ], assave=False)
    configfile.grid(row=1, column=1, padx=PADDING, pady=PADDING, in_=fileframe)
    self.configfile = configfile

    buttonframe = tkinter.Frame(frame)
    buttonframe.pack(fill=tkinter.BOTH, padx=PADDING, pady=PADDING)
    helpbutton = tkinter.Button(buttonframe, text=self.translate("button_help"), font=FONT, command=self._help)
    helpbutton.pack(side=tkinter.LEFT)
    self.helpbutton = helpbutton
    closebutton = tkinter.Button(buttonframe, text=self.translate("button_close"), font=FONT, command=self.destroy)
    closebutton.pack(side=tkinter.RIGHT)
    self.closebutton = closebutton
    executebutton = tkinter.Button(buttonframe, text=self.translate("button_execute"), font=FONT, command=self._execute)
    executebutton.pack(side=tkinter.RIGHT)
    self.executebutton = executebutton

  def serialize (self):
    inputfile = self.inputfile.selectedfile and self.inputfile.selectedfile.absolute()
    configfile = self.configfile.selectedfile and self.configfile.selectedfile.absolute()
    outputfile = self.outputfile.selectedfile and self.outputfile.selectedfile.absolute()
    return {
      "inputfile": inputfile and str(inputfile),
      "configfile": configfile and str(configfile),
      "outputfile": outputfile and str(outputfile),
    }

  @classmethod
  def deserialize (cls, params, *, config, language, serializefile=None): #tmp
    return cls(
      config=config, 
      language=language, 
      defaultinputfile=params.get("inputfile", None), 
      defaultconfigfile=params.get("configfile", None), 
      defaultoutputfile=params.get("outputfile", None), 
      serializefile=serializefile,
    ) 

  def serialize_to_file (self, file):
    with open(file, "w", encoding="utf-8") as stream:
      json.dump(self.serialize(), stream)

  @classmethod
  def deserialize_from_file (cls, file, *, config, language): #tmp
    with open(file, "r", encoding="utf-8") as stream:
      params = json.load(stream)
      return cls.deserialize(params, config=config, language=language, serializefile=file)
