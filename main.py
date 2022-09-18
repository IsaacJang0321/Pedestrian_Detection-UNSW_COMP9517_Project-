# Main file for 9517 projecting coding
# Edit by:
#           z5300114 Zhitong Chen
#           z5211077 Shu Wang
#           z5245818 Nan Du
#           z5286005 Yunseok Jang
#           z5355419 Chenming Yuan

from bg_sub import create_video, background_sub

#Combine all work from other files to sovle all the tasks
def main():
    #modify this for different dataset
    dir = 'step_images/train/STEP-ICCV21-02/'  
    #create_video(dir)    # Do not need to run this code if you already gerneate the video
    background_sub('project.avi')
    return 




if __name__ == "__main__":
    main()