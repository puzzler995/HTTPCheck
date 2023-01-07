import datetime, yaml
from pathlib import Path
import TermTk as ttk

class Site:
  def __init__(self, name: str, url: str, lastupdate) -> None:
    self.name = name
    self.url = url
    self.lastupdate = lastupdate
    self.laststatus = "..."

class SiteFrame(ttk.TTkFrame):
  def __init__(self, site:Site, *args, **kwargs):
    ttk.TTkFrame.__init__(self,title=site.name, *args, **kwargs)
    ttk.TTkLabel(parent=self, pos=(0,0), text=site.url)
    ttk.TTkLabel(parent=self, pos=(0,1), text=site.laststatus)
    ttk.TTkLabel(parent=self, pos=(0,2), text=site.lastupdate)
    ttk.TTkButton(parent=self, pos=(0,3), border=False, text="Edit")
    ttk.TTkButton(parent=self, pos=(0,4), border=False, text="Delete")
    self.setMinimumHeight(7)
    self.setMinimumWidth(15)

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
    self.sideBarLayout.addWidget(ttk.TTkButton(border=False, text="Sidebar2"))
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
    # for row in range(0,4):
    #   for col in range(2,6):
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
        self.siteList.append(Site(site["name"], site["url"], site["lastupdate"]))


# if __name__=="main":
root = ttk.TTk()
App = HttpCheckApp(root)
App.master.mainloop() 