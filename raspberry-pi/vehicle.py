import math
import cv2
import numpy as np

class Position(object):
    def __init__(self, point, frame):
        self.point = point
        self.frame = frame
        self.speed = None
        self.vector = None
        
        
class MovingObject(object):
    
    def __init__(self, carId, position, startFrame):
        self.id = carId
        self.positions = [position]
        self.startFrame = startFrame
        self.counted = False
        self.speed = None
        
        # generates a random color
        self.color = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
        
        
    def getLastPosition(self):
        return self.positions[-1]
    
    
    def addPosition(self, position, fps):
        if len(positions) > 0:
            lastPosition = self.getLastPosition()
            vector = self.getVector(lastPosition, position)
            position.vector = vector
            position.speed = self.getSpeed(lastPosition, position, fps)
            
        self.positions.append(position)
        
        
    def getVector(self, point1, point2):
        dx = float(point2[0] - point1[0])
        dy = float(point2[1] - point1[1])
        
        distance = math.sqrt(dx**2 + dy**2)
        
        if dy > 0:
            angle = math.degrees(math.atan(-dx/dy))
        elif dy == 0.0:
            if dx < 0.0:
                angle = 90.0
            elif dx > 0:
                angle = -90.0
            else:
                angle = 0.0
        else:
            if dx < 0:
                angle = 180 - math.degrees(math.atan(dx/dy))
            elif dx > 0:
                angle = -180 - math.degrees(math.atan(dx/dy))
            else:
                angle = 180.0
                
        return distance, angle
    
    
    def getSpeed(self, position1, position2, fps):
        frameDiff = position2.frame - position1.frame
        seconds = frameDiff/fps
        
        return self.getVector(position1, position2)[0] / seconds
        

    def draw(self, outputImage):
        for point in self.positions:
            cv2.circle(outputImage, point, 2, self.color, 1)
            #cv2.polylines(outputImage, [np.int32(
        
        #if self.speed:
            #cv2.putText(outputImage, ("%1.2f" % self.speed), cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
            

class MovingObjects(object):
    
    def __init__(self, fps):
        self.fps = fps
        self.validObjects = []
        self.ANGLE_TOLERANCE = 15.0
        
        
    
    def validVector(self, position):
        if 
    
    
            
            