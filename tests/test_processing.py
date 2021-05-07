import unittest
import numpy as np
import cv2
from matplotlib import pyplot as plt, cm as cm
from lib import processing


class TestProcessing(unittest.TestCase):
    def setUp(self):
        with open('tests/photos/Clepsiella pneumonae-Rouge de ruth-P3503_0001.tif', 'rb') as kpneu:
            img = kpneu.read()
            npimg = np.frombuffer(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            #self.source = source[369:3565, 148:4005]
            self.source = source[292:3623, 848:3417]
    def test_density_points(self):
        graysource = processing.prepare_image(self.source)
        densities_gray, maximas_gray, inflections_gray = processing.density_points(graysource)
        self.assertEqual(len(maximas_gray), 3)
        