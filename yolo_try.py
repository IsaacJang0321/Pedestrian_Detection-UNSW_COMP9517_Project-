import sys
import cv2 as cv
import math

'''
Need to read all the txt file, try loop through the yolo txt folder
Loop through the original image folder. Sample in bg_sub create_video function.
DO NOT need to save the boxed image, try imshow them with cv.imshow(30)

'''


dir = 'step_images/train/STEP-ICCV21-02/000001.jpg'
img = cv.imread(dir)
print(img.shape)

# cv.imshow('origin', img)
# cv.waitKey(0)

with open('coord.txt', 'r') as f:
    while True:
        line = f.readline().split()
        if not line:
            break
        center_x = math.floor(float(line[1])*1920)
        center_y = math.floor(float(line[2])*1080)
        width = math.floor(float(line[3])*1920/2)
        height = math.floor(float(line[4])*1080/2)
        # print(center_x)
        # print(center_y)
        # print(height)
        # print(width)
        cv.rectangle(img, (center_x - width , center_y - height), (center_x + width, center_y + height),(0, 0, 255), 1)

f.close()

cv.imshow('origin', img)
cv.waitKey(0)