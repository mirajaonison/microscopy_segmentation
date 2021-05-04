import cv2, numpy as np
from KDEpy import FFTKDE
def extract_contours(graysource):
    """
        Return contours
    """
    histogram = cv2.calcHist([graysource], [0], None, [256], [0, 256])
    value = percentile(histogram, 75)
    # Make a binary mask removing the background
    thr, thr_img = cv2.threshold(graysource, value, 255, cv2.THRESH_BINARY)
    return thr_img
    # Get the points around the plate
    contours,h = cv2.findContours(thr_img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sizes_of_contours = map(lambda x: x.shape[0], contours)
    id_biggest_contour = np.argmax(list(sizes_of_contours))
    return contours[id_biggest_contour]
def density_points(image, n_points=256):
    # Density
    pixel_intensity, intensity_density = FFTKDE(kernel="gaussian", bw="ISJ").fit(image.ravel()).evaluate(n_points)
    # Inflections 
    first_derivative_graph = np.gradient(intensity_density)
    second_derivative_graph = np.gradient(first_derivative_graph)
    maximas = np.where(np.diff(np.sign(first_derivative_graph)) != 0)[0]
    inflections = np.where(np.diff(np.sign(second_derivative_graph)) != 0)[0]
    return ([pixel_intensity, intensity_density],maximas, inflections)
def threshold_on_density(image, inflections, maximas):
    if(len(maximas) != 3):
        raise Exception("The picture is not bimodal")
    idx = (np.abs(inflections - maximas[1])).argmin()
    idx = idx if inflections[idx] < maximas[1] else idx - 1
    lower = int(inflections[idx + 1])
    upper = int(maximas[2])
    # Select foreground
    return cv2.inRange(image, lower, upper)
def prepare_image(image):
    graysource = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(graysource, (3,3), 5)
