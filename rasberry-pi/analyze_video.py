import numpy as np
import cv2

videoFileName = "./2023-11-14-23-04-50_test.h264"
videoReader = cv2.VideoCapture(videoFileName)

outputVideo = "test.avi"
videoWriter_fourcc = cv2.VideoWriter_fourcc(*"XVID")
videoWriter = cv2.VideoWriter(outputVideo, videoWriter_fourcc, 30, (320, 240))

# creates a background subtractor object
backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=25, detectShadows=True)

# create kernel for morphological operation
kernel = np.ones((20,20), np.uint8)

print("Starting...")

while videoReader.isOpened():
    
    status, frame = videoReader.read()
    
    modifiedFrame = frame
    
    # Checks if the frame can be read
    if status:
         videoWriter.write(frame)

    else:
        print("Error reading frame. Exiting...")
        break

    
#     # Create foreground mask
#     foregroundMask = backgroundSubtractor.apply(frame)
#     # Close gaps using closing
#     foregroundMask = cv2.morphologyEx(foregroundMask, cv2.MORPH_CLOSE, kernel)
#     # Remove noise with median blur
#     foregroundMask = cv2.medianBlur(foregroundMask, 5)
#     # if a pixle is < ##, then it is considered black (background) otherwise it's white (foreground) 255 is upper limit
#     _, foregroundMask = cv2.threshold(foregroundMask, 127, 255, cv2.THRESH_BINARY)
#     
#     # find contours in binary image
#     contours, hierarchy = cv2.findContours(foregroundMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
#     
#     areas = [cv2.contourArea(c) for c in contours]
#         
#     if len(areas) > 1:
#         max_index = np.argmax(areas)
#         contour = contours[max_index]
#         x,y,w,h = cv2.boundingRect(contour)
#         cv2.rectangle(modifiedFrame, (x,y), (x+w,y+h), (0,255,0), 3)
        
   
    

videoReader.release()
videoWriter.release()
cv2.destroyAllWindows()


