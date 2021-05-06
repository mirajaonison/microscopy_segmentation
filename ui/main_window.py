# coding: utf-8
import wx, cv2, numpy as np, os, base64, time
from io import BytesIO
from ui import panel_preview as preview, button as button, result_output
from skimage.segmentation import chan_vese
from lib import processing

class MainWindow(wx.Frame):
    preview_panel_y = 0.
    preview_panel_x = 0.
    preview_panel_spacing = 5
    preview_panel_size = None
    preview_panel = None
    default_directory = ""
    source_image = None
    default_image = None
    img_config = None

    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)
        self.img_config = {'FACT_BLUR':0, 'HUE':0, 'SATURATION': 0, 'VALUE':0}
        self.selectedInput = None
        panel = wx.Panel(self)
        # Preview panels
        self.preview_panel_y = 20
        self.preview_panel_x = self.Size[0]*0.25
        self.preview_panel_size = wx.Size(self.Size[0]*0.75, self.Size[0]*0.75)
        default_image = wx.Image(
            self.preview_panel_size[0], self.preview_panel_size[1])
        self.default_image = default_image
        
        self.preview_panel = preview.PanelPreview(panel, wx.Point(self.preview_panel_x, self.preview_panel_y), self.preview_panel_size, "Original", default_image)
        self.preview_panel.image.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        # Buttons
        # Import file  
        import_file_btn = button.Button(panel, "Import File...", wx.Point(
            10, 20), wx.Size(180, 30), "import_file")
        import_file_btn.Bind(wx.EVT_BUTTON, self.open_file_browser)
        # Area limits inputs
        wx.StaticText(panel, label="Bord supérieur gauche", name="blurtext", pos=wx.Point(10, 60))
        self.haut_gauche = result_output.ResultOutput(panel, "haut_gauche", text_holder="Bord haut gauche", size=wx.Size(180, 30), position=wx.Point(10, 80), name="haut_gauche")
        wx.StaticText(panel, label="Bord inférieur droit", name="blurtext", pos=wx.Point(10, 120))
        self.bas_droite = result_output.ResultOutput(panel, "bas_droite", "Bord bas droite", wx.Size(180, 30), wx.Point(10, 140), "bas_droite")
        evaluate_btn = button.Button(panel, "Evaluer", wx.Point(100, 180), wx.Size(80, 30), "evaluate_btn")
        evaluate_btn.Bind(wx.EVT_BUTTON, self.evaluate)
        # Masks
        wx.StaticText(panel, label="Mask points", name="masktext", pos=wx.Point(10, 220))
        self.mask_input = result_output.ResultOutput(panel, "mask_input", "Coordonnées masque", wx.Size(180, 30), wx.Point(10, 240), "mask_input")
        mask_btn = button.Button(panel, "Masquer", wx.Point(100, 280), wx.Size(80, 30), "mask_btn")
        mask_btn.Bind(wx.EVT_BUTTON, self.drawMask)
        # Process
        wx.StaticText(panel, label="Noir,Blanc,Total", name="blurtext", pos=wx.Point(10, 320))
        self.results = result_output.ResultOutput(panel, "result", "Results", wx.Size(180, 30), wx.Point(10, 340), "results")
        process_btn = button.Button(panel, "Calculer", wx.Point(100, 380), wx.Size(80, 30), "save_to_file")
        process_btn.Bind(wx.EVT_BUTTON, self.process)
        reset_btn = button.Button(panel, "Reset", wx.Point(20, 380), wx.Size(80, 30), "reset")
        reset_btn.Bind(wx.EVT_BUTTON, self.reset)

        # Input Bindings
        self.haut_gauche.Bind(wx.EVT_TEXT, self.selectInput)
        self.bas_droite.Bind(wx.EVT_TEXT, self.selectInput)
        self.mask_input.Bind(wx.EVT_TEXT, self.selectInput)

    def open_file_browser(self, event):
        dlg = wx.FileDialog(self, message="Select a picture",
                            defaultDir=self.default_directory,
                            defaultFile="",
                            wildcard="*.tif", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            with open(filepath, 'rb') as image_handle:
                image_buffer = image_handle.read()
            npimg = np.frombuffer(image_buffer, dtype=np.uint8)
            # Ignite
            self.source_image = cv2.imdecode(npimg, 1)
            self.default_image = np.copy(self.source_image)
            self.preview_image(wx.Image(self.transform_ndarray_to_bufferImage(self.source_image)))
    def transform_ndarray_to_bufferImage(self, ndarray):
        copy = cv2.imencode(".tif", ndarray)[1]
        return BytesIO(copy.tostring())

    def preview_image(self, image):
        self.preview_panel.setImage(image)
    def OnLeftDown(self, event):
        """left mouse button is pressed"""
        pt = event.GetPosition()  # position tuple
        rows, cols, channels = self.source_image.shape
        row = int(pt[0]*(rows/self.preview_panel_size[0])) - 60
        col = int(pt[1]*(cols/self.preview_panel_size[1])) + 60
        img = cv2.circle(self.source_image, (row,col), 5, (255,0,0), 20)
        pt = (row,col)
        self.selectedInput.AppendText(str(pt))
        self.preview_image(wx.Image(self.transform_ndarray_to_bufferImage(img)))
    def selectInput(self, event):
        self.selectedInput = event.GetEventObject()
    def process(self, event):
        top = eval(self.haut_gauche.textInput.GetValue())
        bottom = eval(self.bas_droite.textInput.GetValue())
        # Cut image
        cut = np.copy(self.source_image[top[1]:bottom[1], top[0]:bottom[0]])
        # count pixels
        number_pixels = cut.shape[0] * cut.shape[1]
        # bgr2gray
        graysource = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)
        number_white = np.sum((graysource/255).flatten())
        self.results.setValue(f"{number_pixels - number_white},{number_white},{number_pixels}")
    def reset(self, event):
        self.source_image = np.copy(self.default_image)
        self.preview_image(wx.Image(self.transform_ndarray_to_bufferImage(self.source_image)))
    def drawMask(self, event):
        pts = eval(self.mask_input.textInput.GetValue().replace('(',',(')[1:])
        pts = np.asarray(pts)
        pts = pts.reshape(-1,1,2)
        img = cv2.fillPoly(self.source_image, [pts], (0,0,0))
        self.preview_image(wx.Image(self.transform_ndarray_to_bufferImage(img)))
    def evaluate(self, event):
        top = eval(self.haut_gauche.textInput.GetValue())
        bottom = eval(self.bas_droite.textInput.GetValue())
        # Cut image
        cut = np.copy(self.source_image[top[1]:bottom[1], top[0]:bottom[0]])
        # gray2bgr
        graysource = processing.prepare_image(cut)
        densities, maximas, inflections = processing.density_points(graysource)
        densities, maximas, inflections = processing.density_points(graysource)
        try:
            img_thr = processing.threshold_on_density(graysource, inflections, maximas)
        except Exception as exc:
            self.results.setValue(f"{exc.args[0]}")
            return
        self.source_image[top[1]:bottom[1], top[0]:bottom[0]] = cv2.cvtColor(img_thr, cv2.COLOR_GRAY2BGR)
        self.preview_image(wx.Image(self.transform_ndarray_to_bufferImage(self.source_image)))

