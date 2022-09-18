import numpy as np
import cv2
import os
import sys
'''
    Written by Shu Wang (z5211077). 
               Zhitong Chen (z5300114).
    Used to draw box and tracks using output of yolov5_Strongsort
'''


'''
# please SELECT your own path and COMMENT OUT others
'''
# Zhitong's path
test_1_txt_filename = "test_1.txt"
test_1_jpg_dir = "step_images/test/STEP-ICCV21-01/" # path of dir of test 1 images
test_1_out_dir = "output_images/test/test_1/" # output directory


# Shu's path
# test_1_txt_filename = "G:/9517GroupProject/txt_files/test_1.txt"    # path of the txt file
# test_1_jpg_dir = "G:/9517GroupProject/step_images/test/STEP-ICCV21-01/" # path of dir of test 1 images
# test_1_out_dir = "G:/9517GroupProject/output_images/test/test_1/" # output directory

#test_1_txt_filename = "G:/9517GroupProject/txt_files/test_1.txt"    # path of the txt file
# test_2_txt_filename = "G:/9517GroupProject/txt_files/try_1/test_2.txt"
# test_2_jpg_dir = "G:/9517GroupProject/step_images/test/STEP-ICCV21-07/" # path of dir of test 1 images
# test_2_out_dir = "G:/9517GroupProject/output_images/test/test_2/" 

# the txt file has 10 columns, we need to use the first 6 columns
# they are:
# frame id left_top_x left_top_y width 
def detect_and_tracks(txt_filename, jpg_dir, out_dir):
    all_label = [[]]    # change this
    frame_label = []
    original_id_tracked = {}
    new_id = 0
    with open(txt_filename, 'r') as f:
        frame_check = 2 # change this
        while True:
            line = f.readline().split()
            if not line:
                all_label.append(frame_label)
                break
            curr_frame = int(line[0])
            if curr_frame != frame_check:
                all_label.append(frame_label)
                frame_label = []
                frame_check += 1
            id = int(line[1])
            center_x = int(line[2]) + (int(line[4])//2)
            center_y = int(line[3]) + (int(line[5])//2)
            width = int(line[4])
            height = int(line[5])
            if id not in original_id_tracked.keys():
                original_id_tracked[id] = new_id + 1
                frame_label.append([center_x, center_y, width, height, new_id + 1])
                new_id += 1
            else:
                frame_label.append([center_x, center_y, width, height, original_id_tracked[id]])

    # then make tracks
    tracks = {}
    i = 1   # change this
    while i < len(all_label):
        j = 0
        while j < len(all_label[i]):
            if str(all_label[i][j][-1]) not in tracks.keys():
                tracks[str(all_label[i][j][4])] = [[i + 1, all_label[i][j][0], all_label[i][j][1]]]
            else:
                tracks[str(all_label[i][j][4])].append([i + 1, all_label[i][j][0], all_label[i][j][1]])
            j += 1
        i += 1
    
    '''
    while id < max_id:
        for center in tracks[str(id)]:
            # find gap
            # interpolation
            # 1 (0, 0), 2 (), 3 (), 4 (3, 3)
            # => 1 (0, 0), 2 (1, 1), 3 (2, 2), 4 (3, 3)
    '''
    #print("Finish making tracks")
    
    # make unique colour for each id
    max_id = len(original_id_tracked)
    i = 0
    colours = []
    while i < max_id:
        c1 = int(np.random.choice(range(256)))
        c2 = int(np.random.choice(range(256)))
        c3 = int(np.random.choice(range(256)))
        colours.append((c1, c2, c3))
        i += 1

    # print(tracks['1'][190])
    # print(tracks['1'][214])

    # print(tracks['11'][170])
    # print(tracks['11'][171])

    # sys.exit()
    # # Now we could use id to get centers for each frame
    jpg_list = os.listdir(jpg_dir)   # get list of all images
    
    n_frame = 1
    curr_max_n = 0
    while n_frame <= len(all_label):
        img_name = os.path.join(jpg_dir, jpg_list[n_frame-1]) # get path of image
        img = cv2.imread(img_name) # read image
        
        curr_n = 0
        while curr_n < len(all_label[n_frame - 1]):
                    
            center_x = all_label[n_frame - 1][curr_n][0]
            center_y = all_label[n_frame - 1][curr_n][1]
            width = all_label[n_frame - 1][curr_n][2]
            height = all_label[n_frame - 1][curr_n][3]
            id = str(all_label[n_frame - 1][curr_n][4])

            # update current total 
            if int(id) >= curr_max_n:
                curr_max_n = int(id)

            cv2.rectangle(img, (center_x - width//2 , center_y - height//2), 
                              (center_x + width//2 , center_y + height//2), colours[int(id) - 1], 3)
            cv2.putText(img, id, (center_x, center_y - height//2), 0, 1, colours[int(id) - 1], 2)
            curr_n += 1

        
            # find list index in tracks of this id in current frame
            tracked = tracks[id]
            count = 0
            for lis in tracked:
                if lis != [n_frame, center_x, center_y]:
                    count += 1
                else:
                    break
            n_line = count
            frame_count = 0
            # draw tracks start from this frame to prev 30 frames
            while n_line >= 0:
                if n_line >= 1 and frame_count < 30:
                    center_x_curr = int(tracks[id][n_line][1])
                    center_y_curr = int(tracks[id][n_line][2])
                    center_x_prev = int(tracks[id][n_line - 1][1])
                    center_y_prev = int(tracks[id][n_line - 1][2])
                    
                    # draw 30 previous lines
                    cv2.line(img, (center_x_curr, center_y_curr), (center_x_prev, center_y_prev), colours[int(id) - 1], 3, 0)
                n_line -= 1 

                frame_count += 1
 
        
        # add current total and number of person in this frame to the image (2.3 and 2.4)
        cv2.putText(img, "Current Total Number of Persons: " + str(curr_max_n), (10, 30), 0, 1, (0, 100, 50), 2)
        cv2.putText(img, "Number of Persons This Frame: " + str(curr_n), (10, 60), 0, 1, (0, 100, 50), 2)
        
        output_name = out_dir + jpg_list[n_frame-1]
        n_frame += 1
        cv2.imwrite(output_name, img)
        # print process
        if (n_frame + 1) % 50 == 0:
            print(f"Finish making frame {n_frame + 1}/{len(jpg_list)}")
    
    return


def view(test_out_dir):
    dir = test_out_dir
    for image in os.listdir(dir):
        img = cv2.imread(os.path.join(dir, image))

        cv2.imshow('Frame', cv2.resize(img, None, fx=0.5, fy=0.5))
        cv2.waitKey(30)

    return 


# test 1
detect_and_tracks(test_1_txt_filename, test_1_jpg_dir, test_1_out_dir)

# View labelled images
view(test_1_out_dir)