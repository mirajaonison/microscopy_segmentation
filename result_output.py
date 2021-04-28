# coding : utf-8
import wx
class ResultOutput(wx.Panel):
    """
        Panel containing the input text and the label
    """
    textInput = None
    def __init__(self, parent, label, text_holder, size, position, name):
        super(ResultOutput, self).__init__(parent, wx.ID_ANY, position, size, wx.TAB_TRAVERSAL, name)
        #super(ResultOutput, self).__init__(parent, value = text_holder, style = wx.TE_READONLY | wx.TE_CENTER, size=size, pos=position)
        self.textInput = wx.TextCtrl(parent=self, value = text_holder, style=wx.TE_LEFT,size=size) 
    def setValue(self, text):
        self.textInput.SetValue(text)

