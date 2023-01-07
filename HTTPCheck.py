import TermTk as ttk

class HttpCheckApp:
  def __init__(self, master: ttk.TTk) -> None:
    self.master=master
    self.mainLayout = ttk.TTkGridLayout(columnMinHeight=0,columnMinWidth=2)
    self.master.setLayout(self.mainLayout)
    self.sideBarLayout = ttk.TTkVBoxLayout()
    header = ttk.TTkLabel(text="HTTP Status Checker", color=ttk.TTkColor.BOLD+ttk.TTkColor.UNDERLINE)
    self.sideBarLayout.addWidget(header)
    self.sideBarLayout.addWidget(ttk.TTkButton(border=False, text="Sidebar1"))
    self.sideBarLayout.addWidget(ttk.TTkButton(border=False, text="Sidebar2"))
    self.mainLayout.addItem(self.sideBarLayout,0,0,4,1)
    for row in range(0,4):
      for col in range(2,6):
        self.mainLayout.addWidget(ttk.TTkButton(border=True, text=(str(row) + ", " + str(col))), row, col)




root = ttk.TTk()
App = HttpCheckApp(root)
App.master.mainloop()