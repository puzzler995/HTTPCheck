import tkinter as tk
import yaml, datetime
from tkinter import ttk
from pathlib import Path

class Site:
  def __init__(self, name: str, url: str, lastupdate, laststatus) -> None:
    self.name = name
    self.url = url
    self.lastupdate = lastupdate
    self.laststatus = laststatus
    self.frame:SiteFrame = None

class SiteFrame(ttk.LabelFrame):
  def __init__(self, container, site:Site, *args, **kwargs):
    super().__init__(container, text=site.name, *args, **kwargs)
    self.site = site
    self.urllabel = ttk.Label(self, text=self.site.url)
    self.urllabel.pack()
    self.statuslabel = ttk.Label(self, text=self.site.laststatus)
    self.statuslabel.pack()
    self.lastupdatelabel = ttk.Label(self, text=self.site.lastupdate)
    self.lastupdatelabel.pack()
    self.editbutton = ttk.Button(
      self,
      text="Edit"
      #TODO: Edit Command
    )
    self.editbutton.pack()
    self.deletebutton = ttk.Button(
      self,
      text="Delete",
      command = lambda: self.deleteFrame()
    )
    self.deletebutton.pack()
    self.site.frame = self
  def deleteFrame(self):
    self.master.master.deleteSite(self.site)





class HttpCheckApp(tk.Tk):
  def __init__(self) -> None:
    super().__init__()
    self.title("HTTP Status Checker")
    self.dev = False
    self.refreshTime = 0
    self.siteList = []
    self.sidebar = ttk.Frame(self)
    self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
    addBtn = ttk.Button(
      self.sidebar,
      text = "Add Site",
      command=lambda: self.spawnAddSite()
    )
    configBtn = ttk.Button(
      self.sidebar,
      text = "Config"
    )
    quitBtn = ttk.Button(
      self.sidebar,
      text = "Quit",
      command=lambda: self.quitapp()
    )
    quitBtn.pack(side=tk.BOTTOM)
    configBtn.pack(side=tk.BOTTOM)
    addBtn.pack(side=tk.BOTTOM)
    self.loadConfig()
    self.siteframe = ttk.Frame(self)
    self.curx = 0
    self.cury = 0
    for site in self.siteList:
      sframe = SiteFrame(self.siteframe, site)
      sframe.grid(column=self.curx, row=self.cury, padx=5, pady=5)
      self.curx += 1
      if self.curx == 4:
        self.cury += 1
        self.curx = 0
    self.siteframe.pack()
    print("Done!")

  def spawnAddSite(self):
    addSite = AddSiteDialog(self)
    addSite.mainloop()

  def loadConfig(self):
    #TODO: Actually change this to config file location
    configfile = Path.cwd() / "test" / "config.yaml"
    sites = []
    site: Site
    with configfile.open() as file:
      config = yaml.safe_load(file)["config"]
    try: 
      self.dev = config["dev"]
    except:
      pass
    self.refreshTime = config["refreshtime"]
    if config["sites"] is not None:
      for site in config["sites"]:
        self.siteList.append(Site(site["name"], site["url"], site["lastupdate"], site["laststatus"]))
  def saveConfig(self):
    #TODO: Actually change this to config file location
    configfile = Path.cwd() / "test" / "config.yaml"
    sites = []
    site: Site
    for site in self.siteList:
      sites.append({"name": site.name, "url": site.url, "lastupdate": site.lastupdate, "laststatus": site.laststatus})
    config = {"config": {"dev": self.dev, "refreshtime": self.refreshTime, "sites": sites}}
    with configfile.open("w") as file:
      yaml.dump(config, file)
  def quitapp(self):
    self.quit()
  def deleteSite(self, site: Site):
    self.siteList.remove(site)
    site.frame.destroy()
    if self.curx ==0:
      if self.cury != 0:
        self.cury -= 1
        self.curx = 3
    else:
      self.curx -= 1
    self.saveConfig()
  def addSite(self, name, url):
    site = Site(name, url, datetime.datetime(1971,1,1,0,0,0), "...")
    self.siteList.append(site)
    sframe = SiteFrame(self.siteframe, site)
    sframe.grid(column=self.curx, row=self.cury, padx=5, pady=5)
    self.curx += 1
    if self.curx == 4:
      self.cury += 1
      self.curx = 0
    self.saveConfig()
class AddSiteDialog(tk.Tk):
  def __init__(self, parent: HttpCheckApp) -> None:
    super().__init__()
    self.resizable(False, False)
    self.title("Add Site")
    self.parent = parent
    self.name = tk.StringVar()
    self.url = tk.StringVar()
    mainframe = ttk.Frame(self)
    mainframe.pack(padx=10, pady=10, fill='x', expand=True)

    name_label = ttk.Label(mainframe, text="Site Name:")
    name_label.pack(fill='x', expand=True)
    self.name_entry = ttk.Entry(mainframe, textvariable=self.name)
    self.name_entry.pack(fill='x', expand=True)
    self.name_entry.focus()

    url_label = ttk.Label(mainframe, text="URL:")
    url_label.pack(fill='x', expand=True)
    self.url_entry = ttk.Entry(mainframe, textvariable=self.url)
    self.url_entry.pack(fill='x', expand=True)

    save_button = ttk.Button(mainframe, text="Save", command=lambda: self.save_clicked())
    save_button.pack(fill='x', expand = True, pady=10)
  def save_clicked(self):
    #TODO: Input Validation
    name = self.name_entry.get()
    url = self.url_entry.get()
    self.parent.addSite(name, url)
    self.destroy()
    self.quit()
app = HttpCheckApp()
app.mainloop()
app.saveConfig()