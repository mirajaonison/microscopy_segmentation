# coding: utf-8
import wx
class Toggle(wx.ToggleButton):
    def __init__(self, parent, label, position, size, name):
        super(Toggle, self).__init__(parent=parent, id=wx.ID_ANY, label=label, pos=position, size=size, name=name)