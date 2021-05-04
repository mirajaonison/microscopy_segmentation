# coding: utf-8
import wx
class Button(wx.Button):
    def __init__(self, parent, label, position, size, name):
        super(Button, self).__init__(parent=parent, id=wx.ID_ANY, label=label, pos=position, size=size, name=name)