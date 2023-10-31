#!/usr/bin/python3
# Source: https://raspberrypi.stackexchange.com/questions/140727/raspberry-pi-python-picamera2-motion-detection-camera-frame-rate


import time, os
from datetime import datetime

import numpy as np

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from libcamera import controls

TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"
FRAME_RATE = 30

LSIZE = (320, 240)
picam2 = Picamera2()

video_config = picam2.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"}, lores={
                                                 "size": LSIZE, "format": "YUV420"})
picam2.configure(video_config)
picam2.start_preview()
encoder = H264Encoder(2000000, repeat=True)
encoder.output = CircularOutput()
picam2.encoder = encoder

picam2.set_controls({"FrameRate": FRAME_RATE})
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

picam2.start()
picam2.start_encoder()

w, h = LSIZE
prev = None
encoding = False
ltime = 0

while True:
    cur = picam2.capture_buffer("lores")
    cur = cur[:w * h].reshape(h, w)
    if prev is not None:
        # Measure pixels differences between current and previous frame
        mse = np.square(np.subtract(cur, prev)).mean()
        if mse > 7:
            if not encoding:
                filename = datetime.now().strftime(TIME_FORMAT)
                encoder.output.fileoutput = f"{filename}.h264"
                encoder.output.start()
                encoding = True
                print("New Motion", mse)
            ltime = time.time()
        else:
            if encoding and time.time() - ltime > 5.0:
                encoder.output.stop()
                encoding = False
                time.sleep(1)
    prev = cur

picam2.stop_encoder()