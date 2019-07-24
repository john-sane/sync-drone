import cv2 as cv
import numpy as np
import time


class YawDetection:
    def __init__(self, visual_feedback=True, src=0, width=640, height=480, fps=15):
        self.cap = cv.VideoCapture(src)
        self.visual_feedback = visual_feedback
        # set fps
        self.cap.set(cv.CAP_PROP_FPS, fps)
        # set dimensions
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
        # self.testingFPS()

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

    def getDimensions(self):
        print("width: ", self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("height: ", self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    @staticmethod
    def houghCircles(src, frame):
        circles = cv.HoughCircles(src,
                                  method=cv.HOUGH_GRADIENT,
                                  dp=1,
                                  minDist=frame.shape[0] / 64,
                                  param1=30,
                                  param2=45,
                                  minRadius=0,
                                  maxRadius=0)
        if circles is not None:
            return circles
        else:
            # toDO: if no circles found
            # quit()
            return None

    @staticmethod
    def drawCircles(frame, circles):
        # Draw detected circles
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.uint16(np.around(circles))

            # loop over the (x, y) coordinates and radius
            for (x, y, r) in circles[0, :]:
                # draw the circle in the output image
                cv.circle(frame, (x, y), r, (0, 255, 0), 2)

    def regionExtraction(self, gray, circles):
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.uint16(np.around(circles))

            # loop over the (x, y) coordinates and radius
            for (x, y, r) in circles[0, :]:

                # region extraction
                p = r - 10
                if (y - p >= 0) and (x - p >= 0):
                    patch = gray[y - p:y + p, x - p:x + p]

                    # calculating the overall gradient
                    sobelx = np.int16(cv.Sobel(patch, cv.CV_64F, 1, 0, ksize=7))
                    sobely = np.int16(cv.Sobel(patch, cv.CV_64F, 0, 1, ksize=7))

                    # calculate the main gradient direction (simply sum all gradients and see where it points)
                    sumGrad_x = np.sum(sobelx)
                    sumGrad_y = np.sum(sobely)

                    angle = np.arctan2(sumGrad_y, sumGrad_x)
                    angle_degree = np.rad2deg(angle)

                    # draw this into the image (from the center)
                    x = np.uint16(patch.shape[0] / 2)
                    y = np.uint16(patch.shape[1] / 2)
                    length = 40

                    endx = np.uint16(x + (length * np.cos(angle)))
                    endy = np.uint16(y + (length * np.sin(angle)))

                    cv.line(patch, (x, y), (endx, endy), (0, 0, 0), thickness=2, lineType=cv.LINE_AA)

                    # testing
                    """print("gradX: " + str(sumGrad_x))
                    print("gradY: " + str(sumGrad_y))"""
                    print("angle RAD: " + str(angle))
                    print("angle DEGREE: " + str(angle_degree))
                    print("patch.shape[0]: " + str(patch.shape[0]))
                    print("patch.shape[1]: " + str(patch.shape[1]))
                    """print("P1: " + str(x) + ", " + str(endx))
                    print("P2: " + str(y) + ", " + str(endy))"""

                    if self.visual_feedback:
                        cv.imshow('patch', patch)
                    return angle
                else:
                    print('patch not in image')
                    return None

    def drawWindows(self, frame, gray, edges, circles):
        # show windows
        cv.imshow('frame', frame)
        self.drawCircles(frame, circles)
        cv.imshow('gray', gray)
        cv.imshow('edges', edges)

    def initVideocapture(self):
        if self.cap is None or not self.cap.isOpened():
            print("no Video capture found")
            self.cap.release()
            return False
        else:
            print("Video capture found")
            return True

    def closeVideocapture(self):
        self.cap.release()
        cv.destroyAllWindows()

    def getAngle(self):
        # read frame by frame
        ret, frame = self.cap.read()

        if frame is not None:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray, 50, 250)
            circles = self.houghCircles(edges, frame)
            angle = self.regionExtraction(gray, circles)

            if self.visual_feedback:
                self.drawWindows(frame, gray, edges, circles)
            else:
                self.cap.release()
                cv.destroyAllWindows()

            return angle
