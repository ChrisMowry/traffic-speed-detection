import numpy as np
import cv2
import os, sys, time
from lock import isLocked

PROCESSED_DIR = "./processed_videos/"


def processFrame(videoWriter, backgroundSubtractor, frame):
    # Create foreground mask
    foregroundMask = backgroundSubtractor.apply(frame)
    # Close gaps using closing
    foregroundMask = cv2.morphologyEx(foregroundMask, cv2.MORPH_CLOSE, kernel)
    # Remove noise with median blur
    foregroundMask = cv2.medianBlur(foregroundMask, 5)
    # if a pixle is < ##, then it is considered black (background) otherwise it's white (foreground) 255 is upper limit
    _, foregroundMask = cv2.threshold(foregroundMask, 127, 255, cv2.THRESH_BINARY)
     
    # find contours in binary image
    contours, hierarchy = cv2.findContours(foregroundMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
     
    areas = [cv2.contourArea(c) for c in contours]
         
    if len(areas) > 1:
        max_index = np.argmax(areas)
        contour = contours[max_index]
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)        
            
        videoWriter.write(frame)

def monitor_dir(dir):
    print("Monitoring {0}".format(dir))
    while(True):

        # Checks for files in the directory
        if(len(os.listdir(dir)) > 0):
            for item in os.listdir(dir):             
                inputVideoFileName = item.split(".")[0]
                inputVideoFile = os.path.join(dir, item)
                if (os.path.splitext(item)[-1].lower() == ".h264") and not isLocked(inputVideoFile):
                    # Processes each video
                    print("Processing {0}...".format(item))
                    processedVideoFile = os.path.join(PROCESSED_DIR, "{0}_processed.avi".format(inputVideoFileName))
                    analyze_video(inputVideoFile, processedVideoFile)
                    os.remove(inputVideoFile)
                else:
                    continue


if __name__ == "__main__":
    #if len(sys.argv) < 2:
        #print("No directory to monitor was provided")
    #else:
        #monitor_dir(sys.argv[1])
    monitor_dir("./videos")
