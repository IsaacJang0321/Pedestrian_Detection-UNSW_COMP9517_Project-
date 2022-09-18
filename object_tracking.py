import numpy as np
import cv2 as cv
import math
import os
from natsort import natsorted

#Sort file in dir numerically
dir = 'yolov5s_test_video_and_labels/exp20/labels'
lst = os.listdir(dir)
list_of_files = natsorted(lst)

#Get labels
all_label = []
for file in list_of_files:
    filename = os.path.join(dir, file)
    frame_label = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline().split()
            if not line:
                break
            center_x = math.floor(float(line[1])*1920)
            center_y = math.floor(float(line[2])*1080)
            width = math.floor(float(line[3])*1920/2)
            height = math.floor(float(line[4])*1080/2)
            frame_label.append([center_x, center_y, width, height])
    f.close()
    all_label.append(frame_label)

cap = cv.VideoCapture('yolov5s_test_video_and_labels/exp20/project.avi')

def draw_path(tracking, frame):
    for object_id, centers in tracking.items():
        length = len(centers)
        count = 0
        for center in centers:
            end_point = count + 1
            if end_point == length:
                break
            cv.line(frame, center, centers[end_point], (255,0,0), 1, 0)
            count += 1
    return


#Loop through frames
count = 0
prev_tracked = []
tracked = {}
tracking = {}
id = 0
tracked_list = []
colors = {}
while True:
    ret, frame = cap.read()
    curr_tracked = []
    if not ret:
        break
    labels = all_label[count]
    for label in labels:
        tracked_list.append([label[0], label[1]])
        curr_tracked.append([label[0], label[1]])

        cv.rectangle(frame, (label[0] - label[2] , label[1] - label[3]), (label[0] + label[2], label[1] + label[3]),(0, 0, 255), 2)

    # Draw all tracked centered point on the graph
    # for center in tracked_list:
    #     cv.circle(frame, (center[0], center[1]), 3, (0, 255, 0), -1)
    if count <= 1:
        for center in curr_tracked:
            for center2 in prev_tracked:
                distance = math.hypot(center2[0] - center[0], center2[1] - center[1])

                if distance < 20:
                    tracked[id] = center
                    tracking[id] = [center, center2]
                    id += 1
    else:
        tracked_copy = tracked.copy()
        curr_tracked_copy = curr_tracked.copy()
        for object_id, center2 in tracked_copy.items():
            exist = False
            for center in curr_tracked_copy: 
                
                distance = math.hypot(center2[0] - center[0], center2[1] - center[1])

                if distance < 20:
                    tracked[object_id] = center
                    tracking[object_id].append(center)
                    exist = True
                    if center in curr_tracked:
                        curr_tracked.remove(center)
                    continue
                
            if not exist:
                tracked.pop(object_id)
                tracking.pop(object_id)

        for center in curr_tracked:
            tracked[id] = center
            tracking[id] = [center]
            id += 1


    for object_id, center in tracked.items():
        cv.circle(frame, (center[0], center[1]), 3, (0, 255, 0), -1)
        cv.putText(frame, str(object_id), (center[0], center[1]-5), 0, 1, (0,0,255),2)
        #cv.rectangle(frame, (label[0] - label[2] , label[1] - label[3]), (label[0] + label[2], label[1] + label[3]),(0, 0, 255), 2)

    draw_path(tracking, frame)
    # print(f"Frame {count}")
    # print("Tracked")
    # print(tracked)
    # print("tracking")
    # print(tracking)
    # print()

    prev_tracked = curr_tracked.copy()
    cv.imshow('Frame', cv.resize(frame, None, fx=0.5, fy=0.5))
    cv.waitKey(0)
    count += 1

cap.release()
cv.destroyAllWindows()
