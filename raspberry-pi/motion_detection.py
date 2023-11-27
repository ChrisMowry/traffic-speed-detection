#!/usr/bin/python3
# Source: https://raspberrypi.stackexchange.com/questions/140727/raspberry-pi-python-picamera2-motion-detection-camera-frame-rate


import time, os
from datetime import datetime
import asyncio

import numpy as np
import cv2

from picamera2 import Picamera2, Preview, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from libcamera import controls


PROCESSED_DIR = "./processed_videos/"

async def processFrame(videoWriter, backgroundSubtractor, kernel, frame):
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
        

async def processContent(queue):
    while(True):
        #await asyncio.sleep(0.1)
        inputVideoFile = await queue.get()
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
        backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=25, detectShadows=True)

        # create kernel for morphological operation
        kernel = np.ones((20,20), np.uint8)

        print("Reading {0}...".format(os.path.basename(inputVideoFile)))
        while videoReader.isOpened():
    
            status, frame = videoReader.read()
    
            # Checks if the frame can be read
            if status:
                await processFrame(videoWriter, backgroundSubtractor, kernel, frame)
            else:
                break

        print("Finished!")

        videoReader.release()
        videoWriter.release()
        os.remove(inputVideoFile)
        
async def detectMotion(queue):
    TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"
    FRAME_RATE = 30
    LSIZE = (320, 240)
    w, h = LSIZE
    picam2 = Picamera2()
    
    # Configures the camera and video
    video_config = picam2.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"}, lores={"size": LSIZE, "format": "YUV420"})
    picam2.configure(video_config)
    encoder = H264Encoder(2000000, repeat=True)
    picam2.encoder = encoder

    # Starts the camera
    picam2.start()
    picam2.set_controls({"FrameRate": FRAME_RATE})
    # Not supported by Rasberry Pi Camera Module v2
    #picam2.set_controls({"AfMode": 0, "LensPosition": 425})

    # allow camera to start up
    await asyncio.sleep(0.5)

    prevFrame = None
    encoding = False
    ltime = 0
    videoFileName = ""
    
    while(True):   
        array = picam2.capture_array()
        
        currentFrame = picam2.capture_buffer("lores")
        currentFrame = currentFrame[:w * h].reshape(h, w)
    
        if prevFrame is not None:
            pixelDiff = np.square(np.subtract(currentFrame, prevFrame)).mean()
            #if pixelDiff > 7:
            print(f"Pixel Difference : {pixelDiff}")
            if pixelDiff > 7: 
                if not encoding:
                    videoFileName = "./videos/{0}.h264".format(datetime.now().strftime(TIME_FORMAT))
                    encoder.output = FileOutput(videoFileName)
                    picam2.start_encoder(encoder)
                    encoding = True
                    print("Motion Detected!", pixelDiff)

                ltime = time.time()
            else:
                if encoding and time.time() - ltime > 2.0:
                    picam2.stop_encoder()
                    encoding = False
                    await queue.put(videoFileName)

                await asyncio.sleep(0.5)
            
        prevFrame = currentFrame
    
    picam2.stop()

async def startWatching():
    print("Waiting for motion...")
    queue = asyncio.Queue()
    await asyncio.gather(detectMotion(queue), processContent(queue))    


if __name__ == "__main__":

    asyncio.run(startWatching())