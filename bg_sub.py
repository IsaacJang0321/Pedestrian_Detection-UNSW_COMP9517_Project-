# Substract the background for each channel
# Input:
#   Original images
# Return:
#   The image which do not contains the background for further modification
#   The image which only contains the background
# Edit by:
#           z5300114 Zhitong Chen

import cv2 as cv
import os
from cv2 import waitKey
import numpy as np

def create_video(dir):
    img_array = []

    for image in os.listdir(dir):
        img = cv.imread(os.path.join(dir, image))
        img_array.append(img)

    height, width, layers = img.shape 
    size = (width,height)

    out = cv.VideoWriter('project.avi',cv.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def background_sub(video):
    #Reading the video
    clip = cv.VideoCapture(video)
    #Generate the background substrator
    fgbg = cv.createBackgroundSubtractorMOG2(history=1000, varThreshold = 14, detectShadows = True)
    #fgbg = cv.createBackgroundSubtractorKNN(history = 2, dist2Threshold=180, detectShadows = True)
    kernel = None
    while True:
        ret, frame = clip.read()   
        if frame is None:
            break

        #Apply background sunstractor 
        fgmask = fgbg.apply(frame)

        #Get ride of the grey show
        _, fgmask = cv.threshold(fgmask, 250, 255, cv.THRESH_BINARY)
        #Get ride of the noise in the background
        fgmask = cv.erode(fgmask, None, iterations=1)
        fgmask = cv.dilate(fgmask, None, iterations=2)

        # Detect contours in the frame.
        contours, _ = cv.findContours(fgmask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # Create a copy of the frame to draw bounding boxes around the detected cars.
        frameCopy = frame.copy()

        for cnt in contours:
        
            # Make sure the contour area is somewhat higher than some threshold to make sure its a car and not some noise.
            if cv.contourArea(cnt) > 500:
                
                # Retrieve the bounding box coordinates from the contour.
                x, y, width, height = cv.boundingRect(cnt)
                
                # Draw a bounding box around the car.
                cv.rectangle(frameCopy, (x , y), (x + width, y + height),(0, 0, 255), 2)
                
                # Write Car Detected near the bounding box drawn.
                cv.putText(frameCopy, 'People', (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1, cv.LINE_AA)
        
        fgmask = cv.cvtColor(fgmask, cv.COLOR_GRAY2BGR)
        # Stack the original frame, extracted foreground, and annotated frame. 
        stacked = np.hstack((fgmask, frameCopy))
        cv.imshow('Extracted Foreground, Detected people', cv.resize(stacked, None, fx=0.3, fy=0.3))
        
        keyboard = cv.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break

    clip.release()
    cv.destroyAllWindows()

