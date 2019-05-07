import cv2 as cv
import numpy as np

patch = 0
cap = cv.VideoCapture(0)

while True:
    # capture frame-by-frame
    ret, frame = cap.read()

    # operations on the frame:

    # greyscale
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # scale
    # img_scaled = cv.resize(img_gray, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)

    # canny edge detection
    edges = cv.Canny(img_gray, 100, 150)

    # HOUGH TRANSFORM
    # ---> image: The input image
    # ---> method: Detection method
    # ---> dp: the Inverse ratio of accumulator resolution and image resolution
    # ---> mindst: minimum distance between centers od detected circles
    # ------> frame.shape: [row , column of pixel, channel]
    # ---> param_1: Upper threshold for the internal Canny edge detector
    # ---> param_2: Threshold for center detection.
    # ---> min_Radius: minimum radius of the circle to be detected.
    # ---> max_Radius: maximum radius to be detected.
    circles = cv.HoughCircles(edges, method=cv.HOUGH_GRADIENT, dp=1, minDist=frame.shape[0] / 64, param1=80, param2=65,
                              minRadius=0, maxRadius=0)
    # Draw detected circles
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.uint16(np.around(circles))

        # loop over the (x, y) coordinates and radius
        for (x, y, r) in circles[0, :]:
            # draw the circle in the output image
            cv.circle(frame, (x, y), r, (0, 255, 0), 2)
            # region extraction
            p = r + 10
            patch = img_gray[y - p:y + p, x - p:x + p]

            # calculating the overall gradient
            sobelx = np.int16(cv.Sobel(patch, cv.CV_64F, 1, 0, ksize=7))
            sobely = np.int16(cv.Sobel(patch, cv.CV_64F, 0, 1, ksize=7))

            # calculate the main gradient direction (simply sum all gradients and see where it points)
            sumGrad_x = np.sum(sobelx)
            sumGrad_y = np.sum(sobely)

            angle = np.arctan2(sumGrad_y, sumGrad_x)

            # draw this into the image (from the center)
            x = np.uint16(patch.shape[0] / 2)
            y = np.uint16(patch.shape[1] / 2)
            length = 40

            endx = np.uint16(x + (length * np.cos(angle)))
            endy = np.uint16(y + (length * np.sin(angle)))

            cv.line(patch, (x, y), (endx, endy), (0, 0, 0), thickness=2, lineType=cv.LINE_AA)

            # testing
            print("gradX: " + str(sumGrad_x))
            print("gradY: " + str(sumGrad_y))
            print("angle: " + str(angle))
            print("patch.shape[0]: " + str(patch.shape[0]))
            print("patch.shape[0]: " + str(patch.shape[1]))
            print("P1: " + str(x) + ", " + str(endx))
            print("P2: " + str(y) + ", " + str(endy))

    cv.imshow('frame', frame)
    cv.imshow('patch', patch)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


