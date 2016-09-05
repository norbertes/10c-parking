# import the necessary packages
import cv2
import numpy as np

cascade_src = './cas1.xml'
car_cascade = cv2.CascadeClassifier(cascade_src)

# grab the raw NumPy array representing the image,
# then initialize the timestamp, and occupied/unoccupied text
image = cv2.imread('./static-image_2048.jpg')

original = np.copy(image)

if image is None:
    print('Can not read/find the image.')
    exit(-1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cars = car_cascade.detectMultiScale(gray,
                                    scaleFactor=1.2,
                                    minNeighbors=3,
                                    minSize=(150, 150),
                                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

for (x, y, w, h) in cars:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

cv2.imshow("Frame", image)

cv2.imwrite('./last_image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 10])

target = open('./last_count.txt', 'w')
target.truncate()
target.write(u'{}'.format(len(cars)))
target.close()
