
import re 
import tkinter as tk 
import tkinter.ttk 
from .scrollable_code import ScrollableCode 

class ScrollableHiyokoScriptCode (ScrollableCode):

  def update_highlight (self, span):
    self.text.tag_config("comment", foreground="gray")
    self.text.tag_config("syntax", foreground="blue")
    self.text.tag_config("variable", foreground="green")
    start, end = self.modrange
    text = self.text.get(start, end)
    for index, line in enumerate(text.split("\n")):
      match = re.match(r"--.*", line) #comment
      if match:
        self.text.tag_add(
          "comment", 
          "{:s} +{:d} lines linestart".format(start, index), 
          "{:s} +{:d} lines lineend".format(start, index),
        )
        continue
      match = re.match(r"#\S*", line) #voice
      if match:
        st, ed = match.span()
        self.text.tag_add(
          "syntax", 
          "{:s} +{:d} lines linestart +{:d} chars".format(start, index, st),
          "{:s} +{:d} lines linestart +{:d} chars".format(start, index, ed),
        )
        self.text.tag_remove(
          "{:s} +{:d} lines linestart +{:d} chars".format(start, index, ed),
          "{:s} +{:d} lines lineend".format(start, index),
        )
        continue 
      match = re.match(r"@\S*", line) #speaker
      if match:
        st, ed = match.span()
        self.text.tag_add(
          "syntax", 
          "{:s} +{:d} lines linestart +{:d} chars".format(start, index, st),
          "{:s} +{:d} lines linestart +{:d} chars".format(start, index, ed),
        )
        self.text.tag_remove(
          "{:s} +{:d} lines linestart +{:d} chars".format(start, index, ed),
          "{:s} +{:d} lines lineend".format(start, index),
        )
        continue 
      match = re.match(r"\$.*", line) #variable 
      if match:
        self.text.tag_add(
          "variable", 
          "{:s} +{:d} lines linestart".format(start, index), 
          "{:s} +{:d} lines lineend".format(start, index),
        )
        continue
      self.text.tag_remove(
        "{:s} +{:d} lines linestart".format(start, index), 
        "{:s} +{:d} lines lineend".format(start, index),
      )
      continue

if __name__ == "__main__": #test
  window = tk.Tk()
  text = ScrollableHiyokoScriptCode(window)
  text.pack(fill=tk.BOTH, expand=True)
  buttonclear = tk.Button(window, text="Clear modified", command=lambda: text.text.set_modified(False))
  buttonclear.pack()
  text.text.set_modified(False)
  text.text.add_onupdate(lambda: window.title("modified={:d}".format(text.text.modified)))
  text.text.call_onupdates() #call manually for initialize window title.
  window.mainloop()
