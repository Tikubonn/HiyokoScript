
import tkinter as tk
import tkinter.ttk as ttk 
import tkinter.font 
from .scrollable_listbox_and_input import ScrollableListboxAndInput
from .config_holder import ConfigHolder 
from .language_holder import LanguageHolder 

class FontSelector:

  def __init__ (self, family, size):
    self._family = family
    self._size = size 
    self._onupdates = list() 

  @property 
  def family (self):
    return self._family 

  @family.setter 
  def family (self, value):
    self._family = value
    self.call_onupdates()

  @property 
  def size (self):
    return self._size 

  @size.setter 
  def size (self, value):
    self._size = value
    self.call_onupdates()

  def add_onupdate (self, func):
    self._onupdates.append(func) 

  def call_onupdates (self):
    for onupdate in self._onupdates:
      onupdate()

  def get_font (self):
    return [ self.family, self.size ]

"""
+---------+
| listbox |
|         |
|         |
+---------+
| input   |
+---------+
"""

class FamilySelectorWidget (ScrollableListboxAndInput):

  def __init__ (self, family, master=None, *, scrollx=False, scrolly=True):
    self.family = family
    super().__init__(master, scrollx=scrollx, scrolly=scrolly)

  def setup_widgets (self):
    super().setup_widgets()
    for family in tk.font.families():
      self.listbox.listbox.insert(tk.END, family)
    self.set_value(self.family)

"""
+---------+
| listbox |
|         |
|         |
+---------+
| input   |
+---------+
"""

class SizeSelectorWidget (ScrollableListboxAndInput):

  def __init__ (self, size, master=None, *, sizerange=(1, 50), scrollx=False, scrolly=True):
    self.size = size
    self.sizerange = sizerange
    super().__init__(master, scrollx=scrollx, scrolly=scrolly)

  def get_value (self):
    try:
      return int(super().get_value()) 
    except ValueError:
      return 0 #return 0 on error.

  def setup_widgets (self):
    super().setup_widgets()
    sizemin = min(self.sizerange)
    sizemax = max(self.sizerange)
    for size in range(sizemin, sizemax):
      self.listbox.listbox.insert(tk.END, str(size))
    self.set_value(self.size)

"""
+---------+
| label   |
+---------+
| input   |
+---------+
"""

class PreviewWidget (ttk.Frame):

  def __init__ (self, master=None, *, width, height):
    super().__init__(master)
    self.width = width
    self.height = height
    self.previewlabel = None 
    self.previewentry = None 
    self.previewvar = None 
    self.setup_widgets()

  def setup_widgets (self):
    previewvar = tk.StringVar(value="abcABC123")
    previewframe = ttk.Frame(self, width=self.width, height=self.height)
    previewframe.pack(fill=tk.X, expand=True)
    previewlabel = ttk.Label(previewframe, textvariable=previewvar, anchor=tk.CENTER, background="#ffffff")
    previewlabel.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
    previewentry = ttk.Entry(self, textvariable=previewvar)
    previewentry.pack(fill=tk.X, expand=True)
    self.previewvar = previewvar
    self.previewlabel = previewlabel
    self.previewentry = previewentry

  def apply_font (self, font):
    self.previewlabel.config(font=font)

"""
+-----------------+
|        [o][_][x]|
+-----------------+
| preview         |
|                 |
+--------+--------+
| family | size   | 
|        |        |
+--------+--------+
|     [ok][cancel]|
+-----------------+
"""

class FontSelectorWindow (tk.Toplevel, ConfigHolder, LanguageHolder):

  def __init__ (self, fontselector, master=None, *, config, language):
    tk.Toplevel.__init__(self, master)
    ConfigHolder.__init__(self, config=config)
    LanguageHolder.__init__(self, language=language)
    self.fontselector = fontselector
    self.preview = None 
    self.familyselector = None 
    self.sizeselector = None 
    self.setup_widgets()

  def _ok (self):
    self.fontselector.family = self.familyselector.get_value()
    self.fontselector.size = self.sizeselector.get_value()
    self.destroy()

  def _onupdate (self):
    self.preview.apply_font((
      self.familyselector.get_value(),
      self.sizeselector.get_value(),
    ))

  def setup_widgets (self): #rough

    #preview 

    previewframe = ttk.Frame(self)
    previewframe.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=10)
    previewlabel = ttk.Label(previewframe, text=self.translate("label_preview"))
    previewlabel.pack(anchor=tk.W)
    preview = PreviewWidget(previewframe, width=320, height=160)
    preview.pack(fill=tk.X)

    #family 

    familyframe = ttk.Frame(self)
    familyframe.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=10)
    familylabel = ttk.Label(familyframe, text=self.translate("label_family"))
    familylabel.pack(anchor=tk.W)
    familyselector = FamilySelectorWidget(self.fontselector.family, familyframe)
    familyselector.pack(fill=tk.BOTH, expand=True)
    familyselector.add_onupdate(self._onupdate)

    #size

    sizeframe = ttk.Frame(self)
    sizeframe.grid(row=1, column=1, sticky=tk.NSEW, padx=10, pady=10)
    sizelabel = ttk.Label(sizeframe, text=self.translate("label_size"))
    sizelabel.pack(anchor=tk.W)
    sizeselector = SizeSelectorWidget(self.fontselector.size, sizeframe)
    sizeselector.pack(fill=tk.BOTH, expand=True)
    sizeselector.add_onupdate(self._onupdate)

    #buttons 

    buttonframe = ttk.Frame(self)
    buttonframe.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)
    cancelbutton = ttk.Button(buttonframe, text=self.translate("label_calcel"), command=self.destroy)
    cancelbutton.pack(side=tk.RIGHT)
    okbutton = ttk.Button(buttonframe, text=self.translate("label_ok"), command=self._ok)
    okbutton.pack(side=tk.RIGHT)

    self.grid_rowconfigure(0, weight=0)
    self.grid_rowconfigure(1, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)

    self.preview = preview
    self.familyselector = familyselector
    self.sizeselector = sizeselector

if __name__ == "__main__": #test
  root = tk.Tk()
  fontselector = FontSelector("メイリオ", 12, config={}, language={ "label_preview": "label_preview", "label_family": "label_family", "label_size": "label_size", "label_calcel": "label_calcel", "label_ok": "label_ok" })
  fontselector.open_window(root)
  root.mainloop()
  print(fontselector.family, fontselector.size) #test
