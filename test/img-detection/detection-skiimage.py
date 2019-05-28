import numpy as np
import matplotlib.pyplot as plt
from skimage import io

from skimage.transform import hough_circle
from skimage.transform import hough_circle_peaks
from skimage.transform import rescale

from skimage.color import rgb2gray
from skimage.util import img_as_ubyte

from skimage.filters import sobel_h
from skimage.filters import sobel_v

from skimage.feature import canny

# Bild einlesen
testImage = io.imread("pics/orientationTest3-4.jpg")

# in Graubild umwandeln
testImageGray = rgb2gray(testImage)

# skalieren
testImageScaled = rescale(testImageGray, 0.5, mode='constant')
testImageUByte = img_as_ubyte(testImageScaled)

# canny
edges = canny(testImageUByte, sigma=2, low_threshold=15, high_threshold=40)

# determine at which radii to search for circles
hough_radii = np.arange(10, 40, 2)

# calculate the result (vote for possible locations...)
hough_res = hough_circle(edges, hough_radii, normalize=True, full_output=False)

# extract the most likely locations where a circle might be...
# big question here: how many to find?
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=3)

# visualize the result
fig, ax = plt.subplots(ncols=1, nrows=1)
for center_y, center_x, radius in zip(cy, cx, radii):
    rect = plt.Circle((center_x, center_y), radius, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

ax.imshow(testImageUByte, cmap=plt.cm.gray)

# region extraction
# for demo, only take the maximum value
x = cx[0];
y = cy[0];
radius = radii[0] - 10;

patch = testImageUByte[y - radius:y + radius, x - radius:x + radius];

# show the patch
fig, ax = plt.subplots(ncols=1, nrows=1)
ax.imshow(patch, cmap=plt.cm.gray)

# calculating the overall gradient
# find out the gradient... (or prewitt?/scharr? => performance?)
gradientImage_h = sobel_h(patch)
gradientImage_v = sobel_v(patch)

# calculate the main gradient direction (simply sum all gradients and see where it points...)
sumGrad_x = np.sum(gradientImage_v)
sumGrad_y = np.sum(gradientImage_h)

print("gradX: " + str(sumGrad_x))
print("gradY: " + str(sumGrad_y))

angle = np.arctan2(sumGrad_y, sumGrad_x)
print("angle: " + str(angle))

# draw this into the image (from the center)
x = patch.shape[0] / 2
y = patch.shape[1] / 2
length = 10

endx = x + (length * np.cos(angle))
endy = y + (length * np.sin(angle))

print("P1: " + str(x) + ", " + str(endx))
print("P2: " + str(y) + ", " + str(endy))

fig, ax = plt.subplots(ncols=1, nrows=1)
ax.imshow(patch, cmap=plt.cm.gray)
ax.plot([x, endx], [y, endy])

plt.show()
