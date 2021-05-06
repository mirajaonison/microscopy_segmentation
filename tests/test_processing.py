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
            self.source = source[369:3565, 148:4005]
    def test_edge(self):
        graysource = cv2.cvtColor(self.source, cv2.COLOR_BGR2GRAY)
        histogram = cv2.calcHist([graysource], [0], None, [256], [0, 256])
        median = processing.percentile(histogram, 50)
        third_percentile = processing.percentile(histogram, 75)
        edges = cv2.Canny(graysource, median, third_percentile)
        cv2.imshow("Edge detection", edges)
        cv2.waitKey(0)