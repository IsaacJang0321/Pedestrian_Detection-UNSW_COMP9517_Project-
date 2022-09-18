import cv2 as cv
import os

# writtern by Shu WANG (z5211077) 2022.07.16


def jpg_to_mp4(in_path, out_path):
    '''
        Change .jpg files from a certain directory to .mp4 video
        in_path: directory of input images
        out_path: directory of the output video
    '''
    dir = in_path # get images
    output = out_path # output path
    num = os.listdir(dir)
    
    img = cv.imread(in_path + '000001.jpg') # read the first image
    height, width, layers = img.shape   # and get the shape of it
    
    fps = 30
    
    fourcc = cv.VideoWriter_fourcc(*'mp4v') # write in .mp4 format
    videowriter = cv.VideoWriter(output, fourcc, fps, (width, height))  # create a video writer object
    
    for counter in range(len(num)):
        # since our input file names are in a certain pattern
        # we need first write this format, then open the image
        if (counter+1) < 10:
            counter_3 = '00' + str(counter+1)
        elif (counter+1) >= 10 and (counter+1) < 100:
            counter_3 = '0' + str(counter+1)
        else:
            counter_3 = str(counter+1)
        path = dir + '000' + str(counter_3) + '.jpg'
        #print(path)
        frame = cv.imread(path) # read the image with image name
        videowriter.write(frame) # write to video

    videowriter.release()

# change your own path
train_dir_1 = "G:/9517GroupProject/step_images/train/STEP-ICCV21-02/"
train_1_out = "G:/9517GroupProject/videos/train/train_1.mp4"
train_dir_2 = "G:/9517GroupProject/step_images/train/STEP-ICCV21-09/"
train_2_out = "G:/9517GroupProject/videos/train/train_2.mp4"
test_dir_1 = "G:/9517GroupProject/step_images/test/STEP-ICCV21-01/"
test_1_out = "G:/9517GroupProject/videos/test/test_1.mp4"
test_dir_2 = "G:/9517GroupProject/step_images/test/STEP-ICCV21-07/"
test_2_out = "G:/9517GroupProject/videos/test/test_2.mp4"
jpg_to_mp4(train_dir_1, train_1_out)
jpg_to_mp4(train_dir_2, train_2_out)
jpg_to_mp4(test_dir_1, test_1_out)
jpg_to_mp4(test_dir_2, test_2_out)
