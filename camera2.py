# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 1
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

cascade_src = './cars.xml'
car_cascade = cv2.CascadeClassifier(cascade_src)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture,
                                       format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image,
    # then initialize the timestamp, and occupied/unoccupied text
    image = frame.array

    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    original = np.copy(image)

    if image is None:
        print('Can not read/find the image.')
        exit(-1)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for (x, y, w, h) in cars:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow("Frame", image)

    cv2.imwrite('./last_image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 10])

    target = open('./last_count.txt', 'w')
    target.truncate()
    target.write(u'{}'.format(len(cars)))
    target.close()
