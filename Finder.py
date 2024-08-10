import tkinter as tk
import tkinter.ttk as ttk
import json
import os
from tkinter.messagebox import askyesno, showinfo
from tkinter.filedialog import askdirectory

GLOBAL_TITLE = "HOI4 Finder"
def opendir():
    init = "C:\\"
    if os.path.exists("C:\\Program Files (x86)\\Steam\\steamapps\\common"):
        init = "C:\\Program Files (x86)\\Steam\\steamapps\\common"
    if os.path.exists("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Hearts of Iron IV"):
        init = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Hearts of Iron IV"
    return askdirectory(initialdir=init)

def selectpath():
    global config_data
    showinfo(GLOBAL_TITLE, "Select HOI4 path")
    while True:
        path = opendir()
        if path[-1] != "/": path+="/"
        if not os.path.isfile(path+"hoi4.exe"):
            if askyesno(GLOBAL_TITLE, "Incorrect path. Do you really want to use it?"):
                config_data["gamepath"] = path
                with open("config.json", "w") as f:
                    json.dump(config_data, f)
                return path
        else:
            config_data["gamepath"] = path
            with open("config.json", "w") as f:
                json.dump(config_data, f)
            return path

class WindowApp:
    def __init__(self, master: tk.Tk=None):
        self.master = master
        self.master.title(GLOBAL_TITLE)
        self.master.resizable(False, False)
        self.MainWindow = ttk.Frame(self.master)
        self.MainWindow.configure(height=200, width=200)

        self.frame3 = ttk.Frame(self.MainWindow)
        self.frame3.configure(height=200, width=200)
        self.label2 = ttk.Label(self.frame3)
        self.label2.configure(text='Game path: ')
        self.label2.grid(column=0, row=0)
        self.pathentry = ttk.Entry(self.frame3)
        self.pathentry.configure(state="readonly", width=50)
        self.pathentry.grid(column=1, row=0)
        self.selectbtn = ttk.Button(self.frame3)
        self.selectbtn.configure(text='Select...')
        self.selectbtn.grid(column=2, row=0)
        self.label4 = ttk.Label(self.frame3)
        self.label4.configure(text='Search: ')
        self.label4.grid(column=0, row=1, sticky="e")
        self.searchentry = ttk.Entry(self.frame3)
        self.searchentry.configure(width=50)
        self.searchentry.grid(column=1, row=1)
        self.searchbtn = ttk.Button(self.frame3)
        self.searchbtn.configure(text='Search')
        self.searchbtn.grid(column=2, row=1)
        self.status = ttk.Label(self.frame3)
        self.status.configure(text='Search something')
        self.status.grid(column=0, columnspan=3, row=2)
        self.frame3.pack(padx=5, pady=5, side="top")
        self.frame4 = ttk.Frame(self.MainWindow)
        self.resultText = tk.Text(self.frame4, height=40, width=40)
        self.scrollbar2 = ttk.Scrollbar(self.frame4)
        self.scrollbar2.configure(orient="vertical")
        self.scrollbar2.pack(anchor="e",expand=False, fill="y", side="right")
        self.scrollbar2.config(command=self.resultText.yview)
        self.resultText.config(yscrollcommand=self.scrollbar2.set)
        self.resultText.pack(expand=False, fill="both", side="top")
        self.resultText.pack_propagate(0)
        self.frame4.pack(padx=5, pady=5, side="top", expand=True, fill="both")
        self.MainWindow.pack(side="top")

        self.pathentry.config(state="normal")
        self.pathentry.delete(0, "end")
        self.pathentry.insert(0, config_data["gamepath"])
        self.pathentry.config(state="readonly")

        self.selectbtn["command"] = self.select_
        self.searchbtn["command"] = self.search

        self.mainwindow = self.MainWindow

    def run(self):
        self.master.mainloop()
    
    def select_(self):
        path = selectpath()
        self.pathentry["state"] = "normal"
        self.pathentry.delete("0", "end")
        self.pathentry.insert("0", path)
        self.pathentry["state"] = "readonly"
    
    def search(self):
        self.resultText.delete("0.0", "end")
        s = self.searchentry.get()
        self.status["text"] = "Searching, wait."
        self.master.update()
        found = 0
        for i in config_data["priority"]:
            tree = os.walk(config_data["gamepath"]+i)
            for path, subdirs, files_ in tree:
                for name in files_:
                    if name.split(".")[-1] in ["txt", "gfx", "gui", "yml"]:
                        with open(path+"/"+name, "r", encoding="utf-8") as f:
                            if s in f.read(): 
                                self.resultText.insert("end", i+path.split(i)[-1].replace("\\", "/")+"/"+name+"\n") #i - line 104
                                self.master.update()
                                found += 1
                    if s in name and name not in self.resultText.get("0.0", "end"):
                        self.resultText.insert("end", "FILENAME: "+i+path.split(i)[-1].replace("\\", "/")+"/"+name+"\n") #i - line 104
                        self.master.update()
                        found += 1
        self.status["text"] = f"Done! {found} matches found."
        

if __name__ == "__main__":

    config_data = {}
    default_config = {"gamepath": "","priority": ["common","history","events","interface","gfx"]}
    try:
        with open("config.json", "r") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        with open("config.json", "w") as f:
            f.write(json.dumps(default_config))
            config_data = default_config
    except json.JSONDecodeError:
        if askyesno(GLOBAL_TITLE, "config.json is broken. Reset it to default config?"):
            with open("config.json", "w") as f:
                f.write(json.dumps(default_config))
                config_data = default_config
        else:
            quit()
    
    if config_data["gamepath"] == "":
        selectpath()
    

    root = tk.Tk()
    app = WindowApp(root)
    app.run()
