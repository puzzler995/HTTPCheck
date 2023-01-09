import datetime, yaml
from pathlib import Path
import TermTk as ttk

class Site:
  def __init__(self, name: str, url: str, lastupdate, laststatus) -> None:
    self.name = name
    self.url = url
    self.lastupdate = lastupdate
    self.laststatus = laststatus
    self.frame = None

class SiteFrame(ttk.TTkFrame):
  def __init__(self, site:Site, *args, **kwargs):
    ttk.TTkFrame.__init__(self,title=site.name, *args, **kwargs)
    self.site = site
    self.urllabel = ttk.TTkLabel(parent=self, pos=(0,0), text=site.url)
    self.statuslabel = ttk.TTkLabel(parent=self, pos=(0,1), text=site.laststatus)
    self.lastupdatelabel = ttk.TTkLabel(parent=self, pos=(0,2), text=site.lastupdate)
    self.editbutton = ttk.TTkButton(parent=self, pos=(0,3), border=False, text="Edit")
    self.deletebutton = ttk.TTkButton(parent=self, pos=(0,4), border=False, text="Delete")
    self.setMinimumHeight(7)
    self.setMinimumWidth(15)
    self.site.frame = self

class HttpCheckApp:
  def __init__(self, master: ttk.TTk) -> None:
    self.master=master
    self.dev = False
    self.refreshTime = 0
    self.siteList = []
    self.mainLayout = ttk.TTkGridLayout(columnMinHeight=0,columnMinWidth=2)
    self.master.setLayout(self.mainLayout)
    self.sideBarLayout = ttk.TTkVBoxLayout()
    header = ttk.TTkLabel(text="HTTP Status Checker", color=ttk.TTkColor.BOLD+ttk.TTkColor.UNDERLINE)
    self.sideBarLayout.addWidget(header)
    self.sideBarLayout.addWidget(ttk.TTkButton(border=False, text="Sidebar1"))
    quitBtn = ttk.TTkButton(border=False, text="Exit")
    quitBtn.clicked.connect(self.quit)
    self.sideBarLayout.addWidget(quitBtn)
    self.mainLayout.addItem(self.sideBarLayout,0,0,4,1)
    self.loadConfig()
    currow = 0
    curcol = 2
    for site in self.siteList:
      self.mainLayout.addWidget(SiteFrame(site), currow, curcol)
      curcol += 1
      if curcol == 6:
        currow += 1
        curcol = 2
    print("Done!")
  def loadConfig(self):
    #TODO: Actually Change this to config file location
    configfile = Path.cwd() / "test" / "config.yaml"
    with configfile.open() as file:
      config = yaml.safe_load(file)["config"]
    try: #This is a try block because I dont intend to leave the dev variable in prod versions of the config file
      self.dev = config["dev"]
    except:
      pass
    self.refreshTime = config["refreshtime"]
    if config["sites"] is not None:
      for site in config["sites"]:
        self.siteList.append(Site(site["name"], site["url"], site["lastupdate"], site["laststatus"]))
  def saveConfig(self):
    #TODO: Actually Change this to config file location
    configfile = Path.cwd() / "test" / "config.yaml"
    sites = []
    site: Site
    for site in self.siteList:
      sites.append({"name": site.name, "url": site.url, "lastupdate": site.lastupdate, "laststatus": site.laststatus})
    config = {"config": {"dev": self.dev, "refreshtime": self.refreshTime, "sites": sites}}
    
    with configfile.open("w") as file:
      yaml.dump(config, file)
  def quit(self):
    self.saveConfig()
    ttk.TTkHelper.quit()

# if __name__=="main":
root = ttk.TTk()
App = HttpCheckApp(root)
App.master.mainloop() 