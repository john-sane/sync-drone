import cv2
import time

cap = cv2.VideoCapture(0)
if cap is None or not cap.isOpened():
    cap.release()
    print('Warning: unable to open video source')

# limit fps
cap.set(cv2.CAP_PROP_FPS, 30)
print("CAP_PROP_FPS", cap.get(cv2.CAP_PROP_FPS))

# testing fps
num_frames = 120
print("Capturing {0} frames".format(num_frames))

start = time.time()

for i in range(0, num_frames):
    ret, frame = cap.read()

end = time.time()

# time elapsed
seconds = end - start
print("Time taken : {0} seconds".format(seconds))

# calculate frames per second
fps = num_frames / seconds
print("Estimated frames per second : {0}".format(fps))

frame_rate = 30
prev = 0

while True:

    time_elapsed = time.time() - prev

    # capture frame-by-frame
    ret, frame = cap.read()

    if time_elapsed > 1./frame_rate:
        prev = time.time()

        # display frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
