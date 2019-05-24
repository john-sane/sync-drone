import cv2 as cv
import numpy as np
import time


class Detection:
    def __init__(self, src):
        self.cap = cv.VideoCapture(src)

    def setup(self):
        self.setFPS(15)
        # self.getFPS()
        self.setDimensions(640, 480)
        # self.getDimensions()
        # self.testingFPS()

    def setFPS(self, fps):
        self.cap.set(cv.CAP_PROP_FPS, fps)

    def getFPS(self):
        print("FPS: ", self.cap.get(cv.CAP_PROP_FPS))

    def testingFPS(self):
        num_frames = 120
        print("Capturing {0} frames".format(num_frames))

        start = time.time()

        for i in range(0, num_frames):
            ret, frame = self.cap.read()

        end = time.time()

        # time elapsed
        seconds = end - start
        print("Time taken : {0} seconds".format(seconds))

        # calculate frames per second
        fps = num_frames / seconds
        print("frames per second : {0}".format(fps))

    def setDimensions(self, width, height):
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    def getDimensions(self):
        print("width: ", self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("height: ", self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    def resize(self, src):
        return cv.resize(src, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)

    def grayScale(self, src):
        return cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    def canny(self, src, threshold_low, threshold_high):
        return cv.Canny(src, threshold_low, threshold_high)

    def regionExtraction(self, gray, circles):
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.uint16(np.around(circles))

            # loop over the (x, y) coordinates and radius
            for (x, y, r) in circles[0, :]:

                # region extraction
                p = r - 10
                patch = gray[y - p:y + p, x - p:x + p]
                if patch is 0:
                    break

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
                """print("gradX: " + str(sumGrad_x))
                print("gradY: " + str(sumGrad_y))
                print("angle: " + str(angle))
                print("patch.shape[0]: " + str(patch.shape[0]))
                print("patch.shape[1]: " + str(patch.shape[1]))
                print("P1: " + str(x) + ", " + str(endx))
                print("P2: " + str(y) + ", " + str(endy))"""

                cv.imshow('patch', patch)
                return angle


    def drawCircles(self, frame, circles):
        # Draw detected circles
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.uint16(np.around(circles))

            # loop over the (x, y) coordinates and radius
            for (x, y, r) in circles[0, :]:
                # draw the circle in the output image
                cv.circle(frame, (x, y), r, (0, 255, 0), 2)

    def houghCircles(self, src, frame):
        circles = cv.HoughCircles(src,
                                  method=cv.HOUGH_GRADIENT,
                                  dp=1,
                                  minDist=frame.shape[0] / 64,
                                  param1=30,
                                  param2=64,
                                  minRadius=0,
                                  maxRadius=0)
        if circles is not None:
            return circles
        else:
            # toDO: if no circles found
            # quit()
            return None

    def streaming(self):
        if self.cap is None or not self.cap.isOpened():
            print("no Video capture found")
            self.cap.release()
            quit()
        else:
            while True:
                # read frame by frame
                ret, frame = self.cap.read()

                if ret is not None or frame is not None:
                    gray = self.grayScale(frame)
                    edges = self.canny(gray, 50, 250)
                    circles = self.houghCircles(edges, frame)
                    self.drawCircles(frame, circles)
                    self.regionExtraction(gray, circles)
                    print('ANGLE ==', self.regionExtraction(gray, circles))

                    # show windows
                    cv.imshow('frame', frame)
                    cv.imshow('gray', gray)
                    cv.imshow('edges', edges)
                else:
                    break

                # keyboard interrupt
                if cv.waitKey(100) & 0xFF == ord('q'):
                    break
            self.cap.release()
            cv.destroyAllWindows()
