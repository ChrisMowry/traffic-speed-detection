#!/usr/bin/python3
# Source: https://raspberrypi.stackexchange.com/questions/140727/raspberry-pi-python-picamera2-motion-detection-camera-frame-rate
# save speed-detector.py url here


import time, os
from datetime import datetime

import numpy as np
import cv2

from picamera2 import Picamera2, Preview, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from libcamera import controls

VIDEO_DIR = "./videos"
PROCESSED_DIR = "./processed_videos/"
DELETED = "./deleted"
BOUNDING_BOX_COLOR = (0, 255, 0)
CENTROID_COLOR = (0, 255, 0)

NEIGHBORHOOD_SPEEDLIMIT = 25
ARTERIAL_SPEEDLIMIT = 30

class motionAnalyzer:
    def __init__(self):
        self.centroids = []

    def captureImage(self, imageFileName, frame):
        cv2.imwrite(imageFileName, frame)
    
    
    def getCentroid(self, x,y,w,h):
        centerX = w//2
        centerY = h//2
    
        return (x + centerX, y + centerY)


    def filterMask(self, mask):
        # sets up kernels
        kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
        kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,8))
        kernelDilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    
        # remove noise
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    
        # close holes in contours
        closing = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernelClose)
    
        # merge adjacent blobs
        dilation = cv2.dilate(closing, kernelDilate, iterations=2)
    
        return dilation

    
    def detectMovingObject(self, mask):
        MIN_CONTOUR_WIDTH = 70 #10
        MIN_CONTOUR_HEIGHT = 70 #10
    
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        matches = []
    
        for (i, contour) in enumerate(contours):
            x,y,w,h = cv2.boundingRect(contour)
            contourValid = (w >= MIN_CONTOUR_WIDTH) and (h >= MIN_CONTOUR_HEIGHT)
        
            if not contourValid or not hierarchy[0, i, 3]:
                continue
        
            centroid = self.getCentroid(x,y,w,h)
            matches.append( ((x,y,w,h), centroid) )
        
        return matches


    def processFrame(self, backgroundSubtractor, frame):
    
        processed = frame.copy()
        foregroundMask = backgroundSubtractor.apply(processed)
        foregroundMask = self.filterMask(foregroundMask)
    
        matches = self.detectMovingObject(foregroundMask)
        frameColor = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
    
        for (i, match) in enumerate(matches):
            contour, centroid = match
            self.centroids.append((centroid, frameColor))
        
        
            x,y,w,h = contour
            cv2.rectangle(processed, (x, y), (x+w-1, y+h-1), BOUNDING_BOX_COLOR, 1)
            for savedCentroid in self.centroids:
                cv2.circle(processed, savedCentroid[0], 2, savedCentroid[1], -1)
        
        return processed
 
      
    def processContent(self):
        inputVideoFile = os.path.join(VIDEO_DIR, os.listdir(VIDEO_DIR)[0])
        inputVideoFileName = os.path.basename(inputVideoFile).split(".")[0]
        outputVideoFile = os.path.join(PROCESSED_DIR, "{0}_processed.avi".format(inputVideoFileName))
    
        videoReader = cv2.VideoCapture(inputVideoFile)

        # gets frames per sec & frame size from video file being read
        fps = int(videoReader.get(cv2.CAP_PROP_FPS))
        width = int(videoReader.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(videoReader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (width, height)

        # notifies if there is an error reading the input video file
        if (videoReader.isOpened() == False):
            print("Error opening video file")

        # sets up output video file
        videoWriter_fourcc = cv2.VideoWriter_fourcc(*'XVID')
        videoWriter = cv2.VideoWriter(outputVideoFile, videoWriter_fourcc, fps, size)

        # creates a background subtractor object
        backgroundSubtractor = cv2.createBackgroundSubtractorKNN(detectShadows=True)

        print("Reading {0}...".format(os.path.basename(inputVideoFile)))
        while videoReader.isOpened():
            status, frame = videoReader.read()
            # Checks if the frame can be read
            if not status:
                break
        
            videoWriter.write(self.processFrame(backgroundSubtractor, frame))
            time.sleep(1.0/ videoReader.get(cv2.CAP_PROP_FPS))


        print("Finished!")

        videoReader.release()
        videoWriter.release()
        os.rename(inputVideoFile, os.path.join(DELETED, os.path.basename(inputVideoFile)))
        #os.remove(inputVideoFile)
        
        
if __name__ == "__main__":
    analyzer = motionAnalyzer()
    analyzer.processContent()