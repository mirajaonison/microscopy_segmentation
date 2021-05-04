# python3
import wx
from ui import main_window
app = wx.App()
configurationWindow = main_window.MainWindow(None, title="Mouna", size=wx.Size(800, 600))
configurationWindow.Show()
app.MainLoop()