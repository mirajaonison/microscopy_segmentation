# python3
import wx
import main_window
import wx.lib.inspection
app = wx.App()
configurationWindow = main_window.MainWindow(None, title="Mouna", size=wx.Size(800, 600))
configurationWindow.Show()
wx.lib.inspection.InspectionTool().Show()
app.MainLoop()