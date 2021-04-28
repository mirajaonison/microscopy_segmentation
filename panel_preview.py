import wx
class PanelPreview(wx.Panel):
    image = None
    def __init__(self, parent, pos, size, name, image):
        super(PanelPreview, self).__init__(parent, wx.ID_ANY, pos, size, wx.TAB_TRAVERSAL, name)
        self.setImage(image)
    def setImage(self, image):
        self.image = image
        self.image = self.image.Scale(self.Size[0], self.Size[1], wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(parent=self, bitmap=wx.Bitmap(self.image))