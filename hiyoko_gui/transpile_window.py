
import subprocess
import tkinter as tk  
import tkinter.ttk as ttk 
import tkinterdnd2 as tkdnd 
from pathlib import Path
from .file_selector import FileSelector, FileSelectorWidget
from .config_holder import ConfigHolder 
from .language_holder import LanguageHolder
from .file_serializable import FileSerializable
from .layout import PADDING
from .popen_subwindow import PopenSubWindow

"""
+----------------------------------------+
| title                        [_][O][x] |
+----------------------------------------+
| image                                  |
|                                        |
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

class TranspileWindow (tkdnd.Tk, FileSerializable, ConfigHolder, LanguageHolder):
  
  def __init__ (self, *, config, language, inputfile=None, configfile=None, outputfile=None, historyfile=None):
    tkdnd.Tk.__init__(self)
    ConfigHolder.__init__(self, config=config)
    LanguageHolder.__init__(self, language=language)
    inputf = inputfile if inputfile and Path(inputfile).exists() else None #存在しないファイルならばNoneが再指定される。
    configf = configfile if configfile and Path(configfile).exists() else None #存在しないファイルならばNoneが再指定される。
    outputf = outputfile if outputfile and Path(outputfile).exists() else None #存在しないファイルならばNoneが再指定される。
    self._inputfileselector = FileSelector(inputf, filetypes=[(self.translate("input_file_type"), "*.txt")])
    self._configfileselector = FileSelector(configf, filetypes=[(self.translate("config_file_type"), "*.json")])
    self._outputfileselector = FileSelector(outputf, filetypes=[(self.translate("output_file_type"), "*.exo")])
    self._historyfile = historyfile
    self._headerphotoimagecache = None 
    self.setup_widgets(inputfile=inputfile, configfile=configfile)
    self.title(self.translate("title"))

  def destroy (self):
    try:
      if self._historyfile:
        self.serialize_to_file(self._historyfile)
    finally:
      super().destroy()

  def execute (self):
    if not self._inputfileselector.selectedfile:
      tk.messagebox.showwarning(
        self.translate("warning_input_file_is_unspecified"),
        self.translate("warning_input_file_is_unspecified_desc")
      )
      return #abort!
    if not self._configfileselector.selectedfile:
      tk.messagebox.showwarning(
        self.translate("warning_config_file_is_unspecified"),
        self.translate("warning_config_file_is_unspecified_desc")
      )
      return #abort!
    if not self._outputfileselector.select_file(assave=True):
      return #abort if canceled.
    if not self._outputfileselector.selectedfile:
      tk.messagebox.showwarning(
        self.translate("warning_output_file_is_unspecified"),
        self.translate("warning_output_file_is_unspecified_desc")
      )
      return #abort!
    command = self.get_hiyokoconfig(("hiyoko_script", "hiyoko_script_command"), "HiyokoScript.exe", shouldexists=False).split(" ") + [str(self._inputfileselector.selectedfile.absolute()), "--config-file", str(self._configfileselector.selectedfile.absolute()), "--output-file", str(self._outputfileselector.selectedfile.absolute())]
    popen = subprocess.Popen(command, shell=True, text=True)
    popensubwindow = PopenSubWindow(
      self, 
      popen, 
      title=self.translate("transpile_text_to_exo"), 
      text=self.translate("transpile_text_to_exo_desc"),
      language=self.language,
    )

  def help (self):
    command = ["start", "explorer", "https://github.com/tikubonn/HiyokoScript"]
    subprocess.run(command, shell=True)

  def setup_widgets (self, *, inputfile=None, configfile=None): #rough

    #desc

    headerframe = ttk.Frame(self)
    headerframe.pack(fill=tk.X, padx=PADDING, pady=PADDING)
    self._headerphotoimagecache = tk.PhotoImage(file="picture/HiyokoScriptGUIHeader.png")
    headerimage = tk.Label(headerframe, image=self._headerphotoimagecache)
    headerimage.pack(fill=tk.X)
    headerlabel = ttk.Label(headerframe, text=self.translate("description"), wrap=320, justify=tk.LEFT)
    headerlabel.pack(fill=tk.X)
    
    #files 

    fileframe = ttk.Frame(self)
    fileframe.pack(fill=tk.X, padx=PADDING, pady=PADDING)
    fileframe.grid_rowconfigure(0, weight=1)
    fileframe.grid_rowconfigure(1, weight=1)
    fileframe.grid_columnconfigure(0, weight=0)
    fileframe.grid_columnconfigure(1, weight=1)
    inputfilelabel = ttk.Label(fileframe, text=self.translate("label_input_file"))
    inputfilelabel.grid(row=0, column=0)
    inputfileselector = FileSelectorWidget(self._inputfileselector, fileframe, config=self.config, language=self.language, assave=False)
    inputfileselector.grid(row=0, column=1, sticky=tk.EW)
    configfilelabel = ttk.Label(fileframe, text=self.translate("label_config_file"))
    configfilelabel.grid(row=1, column=0)
    configfileselector = FileSelectorWidget(self._configfileselector, fileframe, config=self.config, language=self.language, assave=False)
    configfileselector.grid(row=1, column=1, sticky=tk.EW)

    #buttons 

    buttonframe = ttk.Frame(self)
    buttonframe.pack(fill=tk.X, padx=PADDING, pady=PADDING)
    helpbutton = ttk.Button(buttonframe, text=self.translate("button_help"), command=self.help)
    helpbutton.pack(side=tk.LEFT)
    closebutton = ttk.Button(buttonframe, text=self.translate("button_close"), command=self.destroy)
    closebutton.pack(side=tk.RIGHT)
    executebutton = ttk.Button(buttonframe, text=self.translate("button_execute"), command=self.execute)
    executebutton.pack(side=tk.RIGHT)

  def serialize (self):
    inputfile = self._inputfileselector.selectedfile and self._inputfileselector.selectedfile.absolute()
    configfile = self._configfileselector.selectedfile and self._configfileselector.selectedfile.absolute()
    outputfile = self._outputfileselector.selectedfile and self._outputfileselector.selectedfile.absolute()
    return {
      "inputfile": inputfile and str(inputfile),
      "configfile": configfile and str(configfile),
      "outputfile": outputfile and str(outputfile),
    }

  @classmethod
  def deserialize (cls, params, file=None, *, config, language): #tmp
    return cls(
      config=config, 
      language=language, 
      inputfile=params.get("inputfile", None), 
      configfile=params.get("configfile", None), 
      outputfile=params.get("outputfile", None), 
      historyfile=file,
    ) 
