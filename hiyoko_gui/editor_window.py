
import subprocess 
import tkinter as tk 
import tkinter.ttk as ttk 
import tkinterdnd2 as tkdnd
import tkinter.messagebox as messagebox
from pathlib import Path 
from .font_selector import FontSelector, FontSelectorWindow 
from .file_selector import FileSelector, FileSelectorWidget
from .scrollable_hiyoko_script_code import ScrollableHiyokoScriptCode
from .config_holder import ConfigHolder 
from .language_holder import LanguageHolder
from .file_serializable import FileSerializable
from .layout import PADDING
from .popen_subwindow import PopenSubWindow

"""
+--------------------------------+
| title                [_][O][x] |
+--------------------------------+
| image                          |
|                                |
+--------------------------------+
| text                           |
|                                |
+--------------------------------+
| config-file [ file ][ select ] |
+--------------------------------+
| [help]    [ execute ][ close ] |
+--------------------------------+
"""

class EditorWindow (tkdnd.Tk, FileSerializable, ConfigHolder, LanguageHolder):

  def __init__ (self, master=None, *, config, language, family="Meiryo UI", size=10, file=None, configfile=None, outputfile=None, historyfile=None):
    tkdnd.Tk.__init__(self, master)
    ConfigHolder.__init__(self, config=config)
    LanguageHolder.__init__(self, language=language)
    self.fontselector = FontSelector(family, size)
    self.fontselector.add_onupdate(self._onupdatefont)
    f = file if file and Path(file).exists() else None #存在しないファイルならばNoneが再指定される。
    configf = configfile if configfile and Path(configfile).exists() else None #存在しないファイルならばNoneが再指定される。
    outputf = outputfile if outputfile and Path(outputfile).exists() else None #存在しないファイルならばNoneが再指定される。
    self._fileselector = FileSelector(f, filetypes=[(self.translate("input_file_type"), "*.txt")])
    self._fileselector.add_onupdate(self._updatetitle)
    self._configfileselector = FileSelector(configf, filetypes=[(self.translate("config_file_type"), "*.json")])
    self._configfileselector.add_onupdate(self._updatetitle)
    self._outputfileselector = FileSelector(outputf, filetypes=[(self.translate("output_file_type"), "*.exo")])
    self._outputfileselector.add_onupdate(self._updatetitle)
    self.historyfile = historyfile
    self.code = None 
    self.bind("<Control-n>", lambda event: self.new())
    self.bind("<Control-o>", lambda event: self.open())
    self.bind("<Control-s>", lambda event: self.save())
    self.bind("<Control-w>", lambda event: self.save_as())
    self.setup_widgets()

  def _ondnd (self, event):
    file = Path(event.data).absolute()
    self._fileselector.selectedfile = file 
    self.reload()

  def _onupdatefont (self):
    self.code.text.config(font=(
      self.fontselector.family,
      self.fontselector.size,
    ))

  def _updatetitle (self):
    if self.code.text.modified:
      modifiedmark = "*"
    else:
      modifiedmark = ""
    if self._fileselector.selectedfile:
      openedfile = Path(self._fileselector.selectedfile).name 
    else:
      openedfile = "Untitled"
    title = "{:s} {:s}{:s}".format(self.translate("title"), modifiedmark, openedfile)
    self.title(title)

  def destroy (self): #override
    if self.code.text.modified:
      answer = messagebox.askyesnocancel(
        self.translate("ask_save_before_close"),
        self.translate("ask_save_before_close_desc"),
      )
      if answer is True:
        if self.save():
          pass
        else:
          return #abort
      elif answer is False:
        pass
      elif answer is None:
        return #abort
    try:
      if self.historyfile:
        self.serialize_to_file(self.historyfile)
    finally:
      super().destroy()

  def reload (self):
    if self._fileselector.selectedfile:
      with open(self._fileselector.selectedfile, "r", encoding="utf-8") as stream:
        self.code.text.delete("1.0", tk.END)
        self.code.text.insert("1.0", stream.read())
      self.code.text.set_modified(False)

  def open (self):
    if self._fileselector.select_file(assave=False):
      with open(self._fileselector.selectedfile, "r", encoding="utf-8") as stream:
        self.code.text.delete("1.0", tk.END)
        self.code.text.insert("1.0", stream.read())
      self.code.text.set_modified(False)

  def save (self):
    if self._fileselector.selectedfile:
      with open(self._fileselector.selectedfile, "w", encoding="utf-8") as stream:
        tex = self.code.text.get("1.0", tk.END)
        stream.write(tex)
      self.code.text.set_modified(False)
      return True #saved
    else:
      return self.save_as()

  def save_as (self):
    if self._fileselector.select_file(assave=True):
      with open(self._fileselector.selectedfile, "w", encoding="utf-8") as stream:
        tex = self.code.text.get("1.0", tk.END)
        stream.write(tex)
      self.code.text.set_modified(False)
      return True #saved
    else:
      return False #not saved

  def execute (self):
    if not self._fileselector.selectedfile:
      tk.messagebox.showinfo(
        self.translate("info_save_file_before_exec"),
        self.translate("info_save_file_before_exec_desc"),
      )
      if not self.save():
        return #abort if canceled.
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
    command = self.get_hiyokoconfig(("hiyoko_script", "hiyoko_script_command"), "HiyokoScript.exe", shouldexists=False).split(" ") + [str(self._fileselector.selectedfile.absolute()), "--config-file", str(self._configfileselector.selectedfile.absolute()), "--output-file", str(self._outputfileselector.selectedfile.absolute())]
    popen = subprocess.Popen(command, shell=True)
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

  def setup_widgets (self):

    #text

    code = ScrollableHiyokoScriptCode(self)
    code.grid(row=1, column=0, sticky=tk.NSEW)
    code.text.add_onupdate(self._updatetitle)
    code.text.drop_target_register(tkdnd.DND_FILES)
    code.text.dnd_bind("<<Drop>>", self._ondnd)
    self.code = code 

    #files 

    fileframe = ttk.Frame(self)
    fileframe.grid(row=2, column=0, sticky=tk.EW, padx=PADDING, pady=PADDING)
    fileframe.grid_rowconfigure(0, weight=1)
    fileframe.grid_columnconfigure(0, weight=0)
    fileframe.grid_columnconfigure(1, weight=1)
    configfilelabel = ttk.Label(fileframe, text=self.translate("label_config_file"))
    configfilelabel.grid(row=0, column=0)
    configfileselector = FileSelectorWidget(self._configfileselector, fileframe, config=self.config, language=self.language)
    configfileselector.grid(row=0, column=1, sticky=tk.EW)
    
    #buttons 

    buttonframe = ttk.Frame(self)
    buttonframe.grid(row=3, column=0, sticky=tk.EW, padx=PADDING, pady=PADDING)
    closebutton = ttk.Button(buttonframe, text=self.translate("button_close"), command=self.destroy)
    closebutton.pack(side=tk.RIGHT)
    execbutton = ttk.Button(buttonframe, text=self.translate("button_execute"), command=self.execute)
    execbutton.pack(side=tk.RIGHT)
    helpbutton = ttk.Button(buttonframe, text=self.translate("button_help"), command=self.help)
    helpbutton.pack(side=tk.LEFT)

    #window

    self.grid_rowconfigure(0, weight=0)
    self.grid_rowconfigure(1, weight=1)
    self.grid_rowconfigure(2, weight=0)
    self.grid_rowconfigure(3, weight=0)
    self.grid_columnconfigure(0, weight=1)

    #menu

    menu = tk.Menu(self)
    filemenu = tk.Menu(menu, tearoff=0)
    filemenu.add_command(label=self.translate("menu_file_open"), command=self.open)
    filemenu.add_command(label=self.translate("menu_file_save"), command=self.save)
    filemenu.add_command(label=self.translate("menu_file_save_as"), command=self.save_as)
    filemenu.add_separator()
    filemenu.add_command(label=self.translate("menu_file_quit"), command=self.destroy)
    textmenu = tk.Menu(menu, tearoff=0)
    textmenu.add_command(label=self.translate("menu_format_font"), command=lambda: FontSelectorWindow(self.fontselector, self, config=self.config, language=self.language))
    execmenu = tk.Menu(menu, tearoff=0)
    execmenu.add_command(label=self.translate("menu_execute"), command=self.execute)
    menu.add_cascade(label=self.translate("menu_file"), menu=filemenu)
    menu.add_cascade(label=self.translate("menu_format"), menu=textmenu)
    menu.add_cascade(label=self.translate("menu_execute"), menu=execmenu)
    self.config(menu=menu)

    #call onupdates

    self.reload()
    self.fontselector.call_onupdates()
    self._fileselector.call_onupdates()
    self._configfileselector.call_onupdates()
    self._outputfileselector.call_onupdates()
    self.code.text.set_modified(False)
    self.code.text.call_onupdates()

  def serialize (self):
    file = self._fileselector.selectedfile and self._fileselector.selectedfile.absolute()
    configfile = self._configfileselector.selectedfile and self._configfileselector.selectedfile.absolute()
    outputfile = self._outputfileselector.selectedfile and self._outputfileselector.selectedfile.absolute()
    return {
      "family": self.fontselector.family,
      "size": self.fontselector.size,
      "file": file and str(file),
      "configfile": configfile and str(configfile),
      "outputfile": outputfile and str(outputfile),
    }

  @classmethod
  def deserialize (cls, params, file=None, *, config, language): #tmp
    return cls(
      config=config, 
      language=language, 
      family=params.get("family", "Meiryo UI"),
      size=params.get("size", 10), 
      file=params.get("file", None),
      configfile=params.get("configfile", None),
      outputfile=params.get("outputfile", None),
      historyfile=file,
    )
