# -*- coding : utf-8 -*-
import wx
class PropertySlider(wx.Slider):
    def __init__(self, parent, value, minValue, maxValue, pos, size, name):
        super(PropertySlider, self).__init__(parent, id=wx.ID_ANY, value=value, minValue=minValue, maxValue=maxValue, pos=pos, size=size, 
        style=wx.SL_LABELS, name=name)