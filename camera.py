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
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
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

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H,S,V = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
    V = V * 2

    hsv_image = cv2.merge([H,S,V])
    image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # plt.figure(), plt.imshow(image)

    # Sobel - Detect edges
    # Dx = cv2.Sobel(image,cv2.CV_8UC1,1,0)
    # Dy = cv2.Sobel(image,cv2.CV_8UC1,0,1)
    # M = cv2.addWeighted(Dx, 1, Dy,1,0)

    # plt.subplot(1,3,1), plt.imshow(Dx, 'gray'), plt.title('Dx')
    # plt.subplot(1,3,2), plt.imshow(Dy, 'gray'), plt.title('Dy')
    # plt.subplot(1,3,3), plt.imshow(M, 'gray'), plt.title('Magnitude')

    # Otsu - Black and white edges
    ret, binary = cv2.threshold(image,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) # cv2.threshold(M,127,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # plt.figure(), plt.imshow(binary, 'gray')

    # Closing - morphological noise removal
    binary = binary.astype(np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20)))
    # Canny - edge detector
    edges = cv2.Canny(binary, 50, 100)
    # plt.figure(), plt.imshow(edges, 'gray')

    # Hough transformation - detect regular particle (transformata Radona)
    lines = cv2.HoughLinesP(edges,15,3.14/180,80,20,10)[0]

    output = np.zeros_like(image, dtype=np.uint8)
    for line in lines:
        cv2.line(output,(line[0],line[1]), (line[2], line[3]), (100,200,50), thickness=2)
    # plt.figure(), plt.imshow(output, 'gray')

    points = np.array([np.transpose(np.where(output != 0))], dtype=np.float32)
    rect = cv2.boundingRect(points)
    # cv2.rectangle(original,(rect[1],rect[0]), (rect[1]+rect[3], rect[0]+rect[2]),(255,255,255),thickness=2)
    # original = cv2.cvtColor(original,cv2.COLOR_BGR2RGB)

    cv2.rectangle(image,(rect[1],rect[0]), (rect[1]+rect[3], rect[0]+rect[2]),(255,255,255),thickness=2)

    # show the frame
    cv2.imshow("Frame", image)
    cv2.imwrite('./last_image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 10])
