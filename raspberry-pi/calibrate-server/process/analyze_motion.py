#!/usr/bin/python3
# Source: https://raspberrypi.stackexchange.com/questions/140727/raspberry-pi-python-picamera2-motion-detection-camera-frame-rate
# save speed-detector.py url here

import time, os, json, sys
import getopt
from datetime import datetime

import numpy as np
import cv2
import getopt
from moving_objects import MovingObjects, SampleZone, ProcessedObject 
from constants import VIDEO_DIR, IMG_DIR, PROCESSED_DIR, PIXEL_TO_INCHES


def obj_dict(obj):
    """ Used to serialize objects in a list"""
    return obj.__dict__

class motionAnalyzer:
    def __init__(self, speedLimit,
                 inchesRatio,
                 sampleZonePercent,
                 displayZone=False,
                 preserveVideos=False,
                 vehicleColor=(0, 255, 0),
                 textColor=(255,255,255),
                 sampleZoneColor=(255, 0, 0)):
        
        self.boundingBoxColor = vehicleColor
        self.centroidColor = vehicleColor
        self.lineColor = vehicleColor
        self.textColor = textColor
        self.sampleZoneColor = sampleZoneColor
        self.sampleZonePercent = sampleZonePercent
        self.speedlimit = speedLimit
        self.inchesRatio = inchesRatio
        self.preserveVideos = preserveVideos
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.displayZone = displayZone
        self.centroids = []


    def captureImage(self, imageFileName, frame, obj):
        """
        Saves an image from a video frame
        """
        # Copy the frame
        stillImage = frame.copy()        
        cv2.imwrite(imageFileName, stillImage)
        
    
    def getCentroid(self, x,y,w,h):
        """
        Returns a centroid for a given x, y width and height
        """
        centerX = w//2
        centerY = h//2
    
        return (x + centerX, y + centerY)
    
    def speedConverter(self, pixelsPerSec):
        """
        Converts the image pixels per second speed value to real-world miles per hour.
        """
        inchesPerSec = pixelsPerSec * PIXEL_TO_INCHES
        translatedInchesPerSec = inchesPerSec * self.inchesRatio
        
        mph = (translatedInchesPerSec * 3600.0) / 63360.0
        
        return mph
        
    def filterMask(self, mask):
        """
        Creates a filter mask of the frame
        """
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
        """
        Detects a moving object in the frame using contours
        """
        MIN_CONTOUR_WIDTH = 10
        MIN_CONTOUR_HEIGHT = 10
    
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


    def processFrame(self, backgroundSubtractor, frame, frameNumber, movingObjectCounter):
        """
        Processes a given frame from video and returns the processed frame and a midline position if crossed.
        """
        captureImage = False
        processed = frame.copy()
        foregroundMask = backgroundSubtractor.apply(processed)
        foregroundMask = self.filterMask(foregroundMask)
        midlinePosition = None
    
        print("Frame #{0}".format(frameNumber))
        matches = self.detectMovingObject(foregroundMask)
        for (i, match) in enumerate(matches):
            contour, centroid = match
            print("\t{}".format({centroid}))
            x,y,w,h = contour
            movingObjectCounter.countObjects(matches, frameNumber, processed)
            midlinePosition = movingObjectCounter.getMidlinePosition(frameNumber)
        
        return processed, midlinePosition
 
      
    def processContent(self):
        """
        Processes the video file and generates processed images, json and video if enabled
        """
        inputVideoFile = os.path.join(VIDEO_DIR, os.listdir(VIDEO_DIR)[0])
        inputVideoFileName = os.path.basename(inputVideoFile).split(".")[0]
        inputVideoDateTime = datetime.fromtimestamp(os.stat(inputVideoFile).st_mtime)
        inputVideoDateTimeString = inputVideoDateTime.strftime("%m/%d/%Y %I:%M %p")
        outputVideoFile = os.path.join(PROCESSED_DIR, "{0}_processed.avi".format(inputVideoFileName))
    
        videoReader = cv2.VideoCapture(inputVideoFile)

        # gets frames per sec & frame size from video file being read
        fps = int(videoReader.get(cv2.CAP_PROP_FPS))
        width = int(videoReader.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(videoReader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (width, height)
        sampleZone = SampleZone(size, self.sampleZonePercent)

        # notifies if there is an error reading the input video file
        if (videoReader.isOpened() == False):
            print("Error opening video file")

        # sets up output video file
        videoWriter_fourcc = cv2.VideoWriter_fourcc(*'XVID')
        videoWriter = cv2.VideoWriter(outputVideoFile, videoWriter_fourcc, fps, size)

        # creates a background subtractor object
        backgroundSubtractor = cv2.createBackgroundSubtractorKNN(detectShadows=True)
        
        movingObjectCounter = None
        frameNumber = -1
        print("Reading {0}...".format(os.path.basename(inputVideoFile)))
        while videoReader.isOpened():
            frameNumber += 1
            print("Processing frame: {0}".format(frameNumber))
            status, frame = videoReader.read()
            
            # Checks if the frame can be read
            if not status:
                break
    
            # Set up sample zone
            if self.displayZone:
                startLine = np.array([[sampleZone.startX, sampleZone.startY],[sampleZone.startX, sampleZone.endY]], np.int32)
                endLine = np.array([[sampleZone.endX, sampleZone.startY],[sampleZone.endX, sampleZone.endY]], np.int32)
                cv2.polylines(frame, [startLine], False, self.sampleZoneColor, 1)
                cv2.polylines(frame, [endLine], False, self.sampleZoneColor, 1)
                        
            if movingObjectCounter is None:
                movingObjectCounter = MovingObjects(fps, sampleZone, frame)
            
            # Process and write the frame to the output video
            processedFrame, midlinePosition = self.processFrame(backgroundSubtractor,
                                               frame,
                                               frameNumber,
                                               movingObjectCounter)
            
            # if the midline is crossed, the frame is saved as an image.
            if midlinePosition != None:
                self.captureImage("{0}{1}.jpg".format(IMG_DIR, frameNumber), frame, midlinePosition)
                
            videoWriter.write(processedFrame)
            time.sleep(1.0/ videoReader.get(cv2.CAP_PROP_FPS))
        
        videoReader.release()
        videoWriter.release()
        
        print("Processing objects...")
        procesedObjects = []
        for obj in movingObjectCounter.movingObjects:
            #frameDistancePercent = (obj.distanceFromStart/videoReader.get(cv2.CAP_PROP_FRAME_WIDTH)) * 100.0
            if obj.midPointPosition != None:
                inputImage = "{0}{1}.jpg".format(IMG_DIR, obj.midPointPosition.frameNumber)
                outputImage = "{0}{1}-{2}.jpg".format(IMG_DIR, inputVideoDateTime.strftime("%Y%m%d_%H%M%S").replace(".",""), obj.id)
                image = cv2.imread(inputImage)
                
                toMidpointPositions = list(filter(lambda x: x.frameNumber <= obj.midPointPosition.frameNumber, obj.positions))
                
                # add bounding box to image
                x,y,w,h = obj.midPointPosition.boundingBox
                cv2.rectangle(image, (x,y), (x+w,y+h), self.boundingBoxColor, 2)
                # add path line to image
                cv2.polylines(image, [np.int32([position.point for position in toMidpointPositions])], False, self.lineColor, 1)
                # add speed to image
                cv2.putText(image, "{:.2f} mph".format(self.speedConverter(obj.speed)), obj.midPointPosition.point, self.font, 3.0, self.textColor, 1)
                # add date time string to image
                cv2.putText(image, inputVideoDateTimeString, (10,60), cv2.FONT_HERSHEY_PLAIN, 3.0, self.textColor, 2)
                
                print("id: {0} positions: {1} last frame:{2} Distance: {3} PxPerSec: {4}".format(obj.id, obj.getPositionCount(), obj.lastFrame, obj.distanceFromStart, obj.speed))
                for position in toMidpointPositions:
                    cv2.circle(image, position.point, 2, self.centroidColor, 1)
                    
                cv2.imwrite(outputImage, image)
                
                # builds the processed object to send to the web service
                processedObject = ProcessedObject(obj.id, inputVideoDateTimeString)
                processedObject.speed = self.speedConverter(obj.speed)
                processedObject.direction = obj.midPointPosition.vector[-1]
                processedObject.image = os.path.join(inputVideoDateTime.strftime("%Y_%m_%d"), os.path.basename(outputImage))
                processedObject.positions = obj.positions

                procesedObjects.append(processedObject)
                os.remove(inputImage)
        
        os.remove(inputVideoFile)
        print(json.dumps(procesedObjects, default=obj_dict))
        
        
if __name__ == "__main__":
    cameraName = 'Camera 1'
    speedLimit = 25.0
    ratio = 1.0
    sampleZonePercent = 20.0
    video = ''
    
    argv = sys.argv[1:]
    
    try:
        options, args = getopt.getopt(argv, 'f:1:', ['camera-name=','speed-limit=','ratio=','sample-zone=','video='])
        
        for name, value in options:
            if name == '--camera-name':
                cameraName = value
            if name == '--speed-limit':
                speedLimit = value
            if name == '--ratio':
                ratio = value
            if name == '--sample-zone':
                sampleZonePercent = value
            if name == '--video':
                video = value

        print('Camera Name: {0} Speed Limit: {1} mph Ratio: {2} Sample Zone: {3}% Video: {4}'.format(cameraName, speedLimit, ratio, sampleZonePercent, video))
            
    except Exception as ex:
        print(ex)
    

    #analyzer = motionAnalyzer(speedLimit=25.0, inchesRatio=1.0, sampleZonePercent=20.0)
    #analyzer.processContent()