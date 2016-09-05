# import the necessary packages
import cv2
import numpy as np

cascade_src = './cars.xml'
car_cascade = cv2.CascadeClassifier(cascade_src)

# grab the raw NumPy array representing the image,
# then initialize the timestamp, and occupied/unoccupied text
image = cv2.imread('./static-image.jpg')

original = np.copy(image)

if image is None:
    print('Can not read/find the image.')
    exit(-1)


hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
H,S,V = hsv_image[:,:,0], hsv_image[:,:,1], hsv_image[:,:,2]
V = V * 3

hsv_image = cv2.merge([H,S,V])
image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Sobel - Detect edges
Dx = cv2.Sobel(image,cv2.CV_8UC1,1,0)
Dy = cv2.Sobel(image,cv2.CV_8UC1,0,1)
M = cv2.addWeighted(Dx, 1, Dy,1,0)

# Otsu - Black and white edges
ret, binary = cv2.threshold(M,127,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Closing - morphological noise removal
binary = binary.astype(np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20)))
# Canny - edge detector
edges = cv2.Canny(binary, 50, 100)

# Hough transformation - detect regular particle (transformata Radona)
lines = cv2.HoughLinesP(edges,10,3.14/180,50,20,10)[0]

output = np.zeros_like(image, dtype=np.uint8)
for line in lines:
    cv2.line(output,(line[0],line[1]), (line[2], line[3]), (100,200,50), thickness=2)

points = np.array([np.transpose(np.where(output != 0))], dtype=np.float32)
rect = cv2.boundingRect(points)
cv2.rectangle(original,(rect[1],rect[0]), (rect[1]+rect[3], rect[0]+rect[2]),(255,255,255),thickness=2)
original = cv2.cvtColor(original,cv2.COLOR_BGR2RGB)

# cv2.rectangle(image,(rect[1],rect[0]), (rect[1]+rect[3], rect[0]+rect[2]),(255,255,255),thickness=2)






cv2.imwrite('./last_image.jpg', original, [int(cv2.IMWRITE_JPEG_QUALITY), 10])

target = open('./last_count.txt', 'w')
target.truncate()
target.write(u'{}'.format(len(lines)))
target.close()
