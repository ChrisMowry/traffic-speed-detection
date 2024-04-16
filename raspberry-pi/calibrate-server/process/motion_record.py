import time, os, subprocess, sys
from datetime import datetime

import numpy as np
import cv2
import getopt

from picamera2 import Picamera2, Preview, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from libcamera import controls

def getPid():
    pidFile = open('.pid','w')
    pidFile.write("{}".format(os.getpid()))
    pidFile.close()

def detectMotion(cameraName, speedLimit, ratio, sampleZonePercent):
    getPid()
    
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
                if encoding and time.time() - ltime > 1.0:
                    picam2.stop_encoder()
                    subprocess.Popen(['python','./process/analyze_motion.py','--camera-name={}'.format(cameraName)
                                      ,'--speed-limit={}'.format(speedLimit), '--ratio={}'.format(ratio),
                                      '--sample-zone={}'.format(sampleZonePercent), '--video={}'.format(videoFileName)])
                    encoding = False
            
        prevFrame = currentFrame
    
    picam2.stop()
    
if __name__ == "__main__":
    cameraName = 'Camera 1'
    speedLimit = 25.0
    ratio = 1.0
    sampleZonePercent = 20.0
    
    argv = sys.argv[1:]
    
    try:
        options, args = getopt.getopt(argv, 'f:1:', ['camera-name=','speed-limit=','ratio=','sample-zone='])
    except:
        print('Error!')
        
    for name, value in options:
        if name == '--camera-name':
            cameraName = value
        if name == '--speed-limit':
            speedLimit = value
        if name == '--ratio':
            ratio = value
        if name == '--sample-zone':
            sampleZonePercent = value
            
    detectMotion(cameraName=cameraName, speedLimit=speedLimit, ratio=ratio, sampleZonePercent=sampleZonePercent)