import numpy as np
import cv2
from matplotlib import pyplot as plt, cm as cm
from lib import processing
from scipy import stats
from skimage import feature
with open('tests/photos/Clepsiella pneumonae-Rouge de ruth-P3503_0001.tif', 'rb') as kpneu:
    img = kpneu.read()
    npimg = np.frombuffer(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    source= source[100:4200, 500:3600]
# Original images
graysource = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
graysource = cv2.GaussianBlur(graysource, (3,3), 5)
densities_gray, maximas_gray, inflections_gray = processing.density_points(graysource)
normalized = cv2.equalizeHist(graysource)
# Thresholding
idx = (np.abs(inflections_gray - maximas_gray[1])).argmin()
idx = idx if inflections_gray[idx] < maximas_gray[1] else idx - 1
lower = int(inflections_gray[idx+1])
upper = int(maximas_gray[2])
# Select foreground
thr_normalized = cv2.inRange(graysource, lower, upper)
# Background removal
fg_normalized = cv2.bitwise_and(graysource, thr_normalized)
thr, thr_img = cv2.threshold(fg_normalized, 155, 255, cv2.THRESH_BINARY)
colored_normalized = cv2.cvtColor(fg_normalized, cv2.COLOR_GRAY2BGR)
contours, hierarchy = cv2.findContours(fg_normalized, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
colors = [(255,0,0), (255,255,255), (255,255,0), (255,0,255),(0,255,255), (0,0,255), (0,255,0)]
sizes_of_contours = map(lambda x: x.shape[0], contours)
id_biggest_contour = np.argmax(list(sizes_of_contours))
for i, cnt in enumerate(contours):
    cv2.drawContours(colored_normalized, [cnt], -1, colors[i%len(colors)], 1)
plt.subplot(3,3,1),plt.imshow(graysource, cmap='gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(3,3,2),plt.plot(densities_gray[1]),plt.plot(maximas_gray,densities_gray[1][maximas_gray],'or'),plt.plot(inflections_gray,densities_gray[1][inflections_gray],'o')
plt.title('Histogram original')
plt.subplot(3,3,3),plt.imshow(normalized, cmap='gray')
plt.title('Normalized')
plt.subplot(3,3,4),plt.hist(fg_normalized.ravel())
plt.title('Histogram foreground')
plt.subplot(3,3,5),plt.imshow(fg_normalized, cmap='gray')
plt.title('Background removed')
plt.subplot(3,3,6),plt.imshow(colored_normalized, cmap='gray')
plt.title('Canny normalized')
plt.subplot(3,3,7),plt.imshow(thr_img, cmap='gray')
plt.title('Clahe'), plt.xticks([]), plt.yticks([])
plt.subplot(3,3,8)
plt.title('Histogram Clahe')
plt.subplot(3,3,9)
plt.title('Blur Clahe')
plt.show()