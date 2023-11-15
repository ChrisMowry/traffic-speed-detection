#!/usr/bin/python3
# Source: https://raspberrypi.stackexchange.com/questions/140727/raspberry-pi-python-picamera2-motion-detection-camera-frame-rate


import time, os
from datetime import datetime

import numpy as np
import cv2

from picamera2 import Picamera2, Preview, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from libcamera import controls

TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"
FRAME_RATE = 30
LSIZE = (320, 240)
picam2 = Picamera2()

video_config = picam2.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"}, lores={"size": LSIZE, "format": "YUV420"})
picam2.configure(video_config)
encoder = H264Encoder(2000000, repeat=True)
picam2.encoder = encoder


picam2.start()
picam2.set_controls({"FrameRate": FRAME_RATE})
# Not supported by Rasberry Pi Camera Module v2
#picam2.set_controls({"AfMode": 0, "LensPosition": 425})

w, h = LSIZE
prevFrame = None
encoding = False
ltime = 0

while(True):
   
    array = picam2.capture_array()
        
    currentFrame = picam2.capture_buffer("lores")
    currentFrame = currentFrame[:w * h].reshape(h, w)
    
    if prevFrame is not None:
        pixelDiff = np.square(np.subtract(currentFrame, prevFrame)).mean()
        if pixelDiff > 10:           
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
            
    prevFrame = currentFrame
    
picam2.stop()