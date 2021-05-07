import numpy as np
import cv2
from matplotlib import pyplot as plt, cm as cm
from lib import processing
# Original (2228, 496)(1714, 674)(1538, 1172)(1369, 1759)(925, 2292)(735, 2968)(791, 3452)(1214, 3650)(1960, 3507)(2572, 3145)(2988, 2503)(3115, 1793)(2967, 1206)(2805, 783)(2537, 599)
# tests/photos/Clepsiella pneumonae-Rouge de ruth-P3503_0001.tif
# Not bimodal

with open('tests/photos/Clepsiella pneumonae-Rouge de ruth-P1180_0006.tif', 'rb') as kpneu:
    img = kpneu.read()
    npimg = np.frombuffer(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    # (, ), (, )
    source= source[292:3623, 848:3417]
    # source= source[100:4200, 500:3600]
# Correct image
graysource = processing.prepare_image(source)
# Calculate density
densities_gray, maximas_gray, inflections_gray = processing.density_points(graysource)
# Remove background
idx = (np.abs(inflections_gray - maximas_gray[0])).argmin()
idx = idx if inflections_gray[idx] < maximas_gray[0] else idx - 1
lower = int(inflections_gray[idx])
upper = int(maximas_gray[0])
outter_membrane = cv2.inRange(graysource, lower, upper)
#inner_membrane = cv2.inRange(graysource, int(maximas_gray[1]), upper)
#negative_out = cv2.inRange(graysource, upper, int(maximas_gray[2]))
hist = cv2.calcHist([graysource], [0], None, [256], [0,256])
""" mask = np.zeros(graysource.shape)
contours, hierarchy = cv2.findContours(outter_membrane, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
sizes_of_contours = map(lambda x: x.shape[0], contours)
id_biggest_contour = np.argmax(list(sizes_of_contours))
cv2.drawContours(mask, [contours[id_biggest_contour]], -1, (255),3)
contours, hierarchy = cv2.findContours(negative_out, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
sizes_of_contours = map(lambda x: x.shape[0], contours)
id_biggest_contour = np.argmax(list(sizes_of_contours))
cv2.drawContours(mask, [contours[id_biggest_contour]], 0, (255),3, cv2.FILLED) """

""" term_criteria = (cv2.TERM_CRITERIA_MAX_ITER, 5, 1.0)
k_means = cv2.kmeans(graysource, 3, None,
                        term_criteria, 10,
                        cv2.KMEANS_PP_CENTERS)"""
plt.subplot(3,2,1),plt.imshow(graysource, cmap='gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
host = plt.subplot(3,2,2)
plt_density = host.twinx()
h = host.hist(graysource.flatten(), label='Histogram')
d, = plt_density.plot(densities_gray[1],color='#002171',label='Density curve')
m, = plt_density.plot(maximas_gray,densities_gray[1][maximas_gray],'o',color='#00867d',label='Maximas')
i, = plt_density.plot(inflections_gray,densities_gray[1][inflections_gray],'o',color='#ab47bc',label='Inflection points')
host.set_ylabel('Number of pixels')
plt_density.set_ylabel('Probabilities of density')
host.set_xlabel('Pixel values')
plt.legend(loc='upper left')
plt.title('Histogram original')
plt.subplot(3,2,3),plt.imshow(outter_membrane, cmap='gray')
plt.title('Around first maxima')
plt.subplot(3,2,4)
plt.title('Organelles')
plt.subplot(3,2,5)
plt.title('Negative out')
plt.subplot(3,2,6)
plt.title('Result')
plt.show()