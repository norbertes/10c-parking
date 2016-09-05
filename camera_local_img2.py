# import the necessary packages
import cv2
import numpy as np

clasificators = ['cars', 'cas1']
clasificator = clasificators[1]

if clasificator is 'cars':
    cascade_src = './cars.xml'
elif clasificator is 'cas1':
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
blurred = cv2.GaussianBlur(gray, (13, 13), 0)

# changed_image = cv2.Canny(blurred, 10, 200)
# edges = cv2.Canny(blurred, 10, 300)

changed_image = cv2.fastNlMeansDenoising(blurred, None, 7, 21, 8)

# changed_image = gray
# cv2.imwrite('./last_image.jpg', changed_image, [int(cv2.IMWRITE_JPEG_QUALITY), 10])


if clasificator is 'cars':
    cars = car_cascade.detectMultiScale(changed_image,
                                        scaleFactor=1.1,
                                        minNeighbors=1,
                                        minSize=(150, 150))

elif clasificator is 'cas1':
    cars = car_cascade.detectMultiScale(changed_image,
                                        scaleFactor=1.1515,
                                        minNeighbors=3,
                                        minSize=(150, 150),
                                        flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

for (x, y, w, h) in cars:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 4)

cv2.imshow("Frame", image)

cv2.imwrite('./last_image.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 10])

target = open('./last_count.txt', 'w')
target.truncate()
target.write(u'{}'.format(len(cars)))
target.close()
